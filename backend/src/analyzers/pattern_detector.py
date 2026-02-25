
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict, Counter
import re
import hashlib
import logging
from datetime import datetime, timedelta

from ..entities import Error

logger = logging.getLogger(__name__)


class PatternDetector:
    """Detects error patterns in code generation"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.min_pattern_occurrences = config.get('min_pattern_occurrences', 3)
        self.similarity_threshold = config.get('similarity_threshold', 0.8)

    def detect_patterns(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns in errors"""
        if len(errors) < self.min_pattern_occurrences:
            return []
        
        patterns = []
        
        # Group by error type
        type_groups = defaultdict(list)
        for error in errors:
            error_type = error.get('error_type', 'unknown')
            type_groups[error_type].append(error)
        
        for error_type, type_errors in type_groups.items():
            if len(type_errors) < self.min_pattern_occurrences:
                continue
            
            # Extract patterns from this error type
            type_patterns = self._extract_patterns_from_type(type_errors)
            patterns.extend(type_patterns)
        
        # Store patterns
        for pattern in patterns:
            pattern_id = self._generate_pattern_id(pattern)
            pattern['pattern_id'] = pattern_id
            self.patterns[pattern_id] = pattern
        
        return patterns

    def _extract_patterns_from_type(
        self,
        errors: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract patterns from errors of same type"""
        patterns = []
        
        # Extract error messages
        messages = [e.get('error_message', '') for e in errors]
        
        # Find common substrings
        common_substrings = self._find_common_substrings(messages)
        
        for substring in common_substrings:
            # Find errors matching this pattern
            matching_errors = [
                e for e in errors
                if substring in e.get('error_message', '')
            ]
            
            if len(matching_errors) >= self.min_pattern_occurrences:
                # Extract variable parts
                variables = self._extract_variables(
                    substring,
                    [e.get('error_message', '') for e in matching_errors]
                )
                
                pattern = {
                    'pattern': substring,
                    'error_type': errors[0].get('error_type'),
                    'occurrences': len(matching_errors),
                    'first_seen': min(e.get('recorded_at', datetime.now()) for e in matching_errors),
                    'last_seen': max(e.get('recorded_at', datetime.now()) for e in matching_errors),
                    'examples': [e.get('error_message') for e in matching_errors[:3]],
                    'variables': variables,
                    'affected_models': list(set(e.get('model_id') for e in matching_errors if 'model_id' in e)),
                    'severity': self._calculate_pattern_severity(matching_errors)
                }
                patterns.append(pattern)
        
        return patterns

    def _find_common_substrings(
        self,
        strings: List[str],
        min_length: int = 10
    ) -> List[str]:
        """Find common substrings across multiple strings"""
        if len(strings) < 2:
            return []
        
        common = set()
        
        # Build suffix array for first string
        s1 = strings[0]
        suffixes = [(s1[i:], i) for i in range(len(s1))]
        suffixes.sort()
        
        # Compare with other strings
        for other in strings[1:]:
            current_common = set()
            
            for suffix, pos in suffixes:
                # Find common prefix with other string
                prefix_len = 0
                while (pos + prefix_len < len(s1) and
                       prefix_len < len(other) and
                       s1[pos + prefix_len] == other[prefix_len]):
                    prefix_len += 1
                
                if prefix_len >= min_length:
                    current_common.add(s1[pos:pos + prefix_len])
            
            if common:
                common &= current_common
            else:
                common = current_common
            
            if not common:
                break
        
        # Filter and sort results
        result = list(common)
        result.sort(key=len, reverse=True)
        
        return result[:10]  # Return top 10 longest patterns

    def _extract_variables(self, pattern: str, messages: List[str]) -> List[str]:
        """Extract variable parts from messages matching pattern"""
        variables = set()
        
        # Create regex pattern with capture groups for variable parts
        # Replace words that vary with capture groups
        words = pattern.split()
        regex_parts = []
        var_positions = []
        
        for i, word in enumerate(words):
            # Check if this word varies across messages
            word_variations = set()
            for msg in messages:
                msg_words = msg.split()
                if i < len(msg_words):
                    word_variations.add(msg_words[i])
            
            if len(word_variations) > 1:
                # This is a variable
                regex_parts.append(r'(\S+)')
                var_positions.append(i)
            else:
                # This is constant
                regex_parts.append(re.escape(word))
        
        regex_str = r'\s+'.join(regex_parts)
        
        # Extract variables from each message
        for msg in messages:
            match = re.search(regex_str, msg)
            if match:
                for j, pos in enumerate(var_positions):
                    var_value = match.group(j + 1)
                    variables.add(var_value)
        
        return list(variables)

    def _calculate_pattern_severity(self, errors: List[Dict[str, Any]]) -> str:
        """Calculate pattern severity based on errors"""
        # Count error severities
        severities = defaultdict(int)
        for error in errors:
            severities[error.get('severity', 'medium')] += 1
        
        if severities.get('critical', 0) > 0:
            return 'critical'
        elif severities.get('high', 0) > len(errors) * 0.3:
            return 'high'
        elif severities.get('medium', 0) > len(errors) * 0.5:
            return 'medium'
        else:
            return 'low'

    def _generate_pattern_id(self, pattern: Dict[str, Any]) -> str:
        """Generate unique pattern ID"""
        pattern_str = f"{pattern['pattern']}_{pattern['error_type']}"
        hash_obj = hashlib.md5(pattern_str.encode())
        return f"pat_{hash_obj.hexdigest()[:8]}"

    def match_error_to_pattern(self, error: Dict[str, Any]) -> Optional[str]:
        """Match an error to existing patterns"""
        error_msg = error.get('error_message', '')
        
        for pattern_id, pattern in self.patterns.items():
            if pattern['pattern'] in error_msg:
                return pattern_id
        
        return None

    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about detected patterns"""
        if not self.patterns:
            return {}
        
        stats = {
            'total_patterns': len(self.patterns),
            'by_severity': defaultdict(int),
            'by_type': defaultdict(int),
            'most_frequent': [],
            'active_patterns': 0
        }
        
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        for pattern in self.patterns.values():
            stats['by_severity'][pattern.get('severity', 'unknown')] += 1
            stats['by_type'][pattern.get('error_type', 'unknown')] += 1
            
            # Check if pattern is still active (seen in last week)
            if pattern.get('last_seen', now) > week_ago:
                stats['active_patterns'] += 1
            
            # Track most frequent
            stats['most_frequent'].append({
                'pattern': pattern['pattern'][:50] + '...' if len(pattern['pattern']) > 50 else pattern['pattern'],
                'occurrences': pattern['occurrences'],
                'severity': pattern.get('severity')
            })
        
        # Sort most frequent
        stats['most_frequent'].sort(key=lambda x: x['occurrences'], reverse=True)
        stats['most_frequent'] = stats['most_frequent'][:10]
        
        return dict(stats)