
from typing import List, Dict, Any, Optional, Tuple
import ast
import difflib
import logging
import numpy as np

from .metric_calculator import MetricCalculator
from ..entities import EvaluationResult, Metric

logger = logging.getLogger(__name__)


class SemanticMetricsCalculator(MetricCalculator):
    """Calculator for semantic similarity metrics"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.supported_metrics = ['codebleu', 'ast_similarity', 'dataflow_match']
        
        # Set normalization rules
        self.set_normalization_rule('codebleu', 0, 1, higher_is_better=True)
        self.set_normalization_rule('ast_similarity', 0, 1, higher_is_better=True)
        self.set_normalization_rule('dataflow_match', 0, 1, higher_is_better=True)
        
        # Set default thresholds
        self.set_threshold('codebleu', 0.6)
        
        # Set default weights
        self.set_weight('codebleu', 0.5)
        self.set_weight('ast_similarity', 0.3)
        self.set_weight('dataflow_match', 0.2)

    def calculate(self, results: List[EvaluationResult]) -> Dict[str, float]:
        """Calculate semantic metrics"""
        if not results:
            return {}
        
        metrics = {}
        
        total_codebleu = 0
        total_ast_sim = 0
        total_dataflow = 0
        count = 0
        
        for result in results:
            if not result.generated_code or not result.metadata.get('reference_code'):
                continue
            
            reference = result.metadata['reference_code']
            generated = result.generated_code
            
            # Calculate CodeBLEU (simplified version)
            codebleu = self._calculate_codebleu(generated, reference)
            total_codebleu += codebleu
            
            # Calculate AST similarity
            ast_sim = self._calculate_ast_similarity(generated, reference)
            total_ast_sim += ast_sim
            
            # Calculate dataflow match
            dataflow = self._calculate_dataflow_match(generated, reference)
            total_dataflow += dataflow
            
            count += 1
        
        if count > 0:
            metrics['codebleu'] = total_codebleu / count
            metrics['ast_similarity'] = total_ast_sim / count
            metrics['dataflow_match'] = total_dataflow / count
        
        return metrics

    def _calculate_codebleu(self, generated: str, reference: str, n_gram: int = 4) -> float:
        """Calculate simplified CodeBLEU score"""
        # This is a simplified version. Full CodeBLEU requires parsing and AST matching
        
        # Tokenize
        gen_tokens = self._tokenize_code(generated)
        ref_tokens = self._tokenize_code(reference)
        
        if not gen_tokens or not ref_tokens:
            return 0.0
        
        # Calculate n-gram precision
        precisions = []
        for n in range(1, min(n_gram + 1, 5)):
            gen_ngrams = self._get_ngrams(gen_tokens, n)
            ref_ngrams = self._get_ngrams(ref_tokens, n)
            
            if not ref_ngrams:
                continue
            
            matches = sum(1 for ng in gen_ngrams if ng in ref_ngrams)
            precision = matches / len(gen_ngrams) if gen_ngrams else 0
            precisions.append(precision)
        
        if not precisions:
            return 0.0
        
        # Geometric mean of precisions
        codebleu = np.exp(np.mean(np.log(precisions + 1e-10)))
        
        # Brevity penalty
        gen_len = len(gen_tokens)
        ref_len = len(ref_tokens)
        
        if gen_len > ref_len:
            bp = 1.0
        else:
            bp = np.exp(1 - ref_len / gen_len) if gen_len > 0 else 0
        
        return codebleu * bp

    def _tokenize_code(self, code: str) -> List[str]:
        """Simple code tokenization"""
        import re
        # Split on whitespace and punctuation
        tokens = re.findall(r'\w+|[^\w\s]', code)
        return [t for t in tokens if t.strip()]

    def _get_ngrams(self, tokens: List[str], n: int) -> List[Tuple[str, ...]]:
        """Get n-grams from tokens"""
        if len(tokens) < n:
            return []
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

    def _calculate_ast_similarity(self, generated: str, reference: str) -> float:
        """Calculate AST similarity"""
        try:
            gen_ast = self._get_ast_structure(generated)
            ref_ast = self._get_ast_structure(reference)
            
            if not gen_ast or not ref_ast:
                return 0.0
            
            # Compare AST structures using sequence matching
            gen_seq = self._ast_to_sequence(gen_ast)
            ref_seq = self._ast_to_sequence(ref_ast)
            
            matcher = difflib.SequenceMatcher(None, gen_seq, ref_seq)
            return matcher.ratio()
            
        except Exception as e:
            logger.debug(f"AST similarity calculation failed: {e}")
            return 0.0

    def _get_ast_structure(self, code: str) -> Optional[ast.AST]:
        """Parse code to AST"""
        try:
            return ast.parse(code)
        except SyntaxError:
            return None

    def _ast_to_sequence(self, tree: ast.AST) -> List[str]:
        """Convert AST to sequence of node types"""
        sequence = []
        for node in ast.walk(tree):
            sequence.append(type(node).__name__)
        return sequence

    def _calculate_dataflow_match(self, generated: str, reference: str) -> float:
        """Calculate dataflow pattern similarity"""
        try:
            gen_flow = self._extract_dataflow(generated)
            ref_flow = self._extract_dataflow(reference)
            
            if not gen_flow or not ref_flow:
                return 0.0
            
            # Compare dataflow patterns
            all_vars = set(gen_flow.keys()) | set(ref_flow.keys())
            if not all_vars:
                return 1.0
            
            matches = 0
            for var in all_vars:
                gen_patterns = gen_flow.get(var, [])
                ref_patterns = ref_flow.get(var, [])
                
                # Compare operation sequences
                matcher = difflib.SequenceMatcher(None, gen_patterns, ref_patterns)
                matches += matcher.ratio()
            
            return matches / len(all_vars)
            
        except Exception as e:
            logger.debug(f"Dataflow match calculation failed: {e}")
            return 0.0

    def _extract_dataflow(self, code: str) -> Dict[str, List[str]]:
        """Extract dataflow patterns from code"""
        flow = {}
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    # Track variable assignments
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            if var_name not in flow:
                                flow[var_name] = []
                            flow[var_name].append('assign')
                            
                elif isinstance(node, ast.AugAssign):
                    # Track augmented assignments
                    if isinstance(node.target, ast.Name):
                        var_name = node.target.id
                        if var_name not in flow:
                            flow[var_name] = []
                        flow[var_name].append('aug_assign')
                        
                elif isinstance(node, ast.BinOp):
                    # Track binary operations
                    for child in ast.walk(node):
                        if isinstance(child, ast.Name):
                            var_name = child.id
                            if var_name not in flow:
                                flow[var_name] = []
                            flow[var_name].append('bin_op')
                            
                elif isinstance(node, ast.Call):
                    # Track function calls
                    for child in ast.walk(node):
                        if isinstance(child, ast.Name):
                            var_name = child.id
                            if var_name not in flow:
                                flow[var_name] = []
                            flow[var_name].append('call')
                            
        except Exception:
            pass
        
        return flow

    def calculate_pairwise_similarity(
        self,
        results: List[EvaluationResult]
    ) -> np.ndarray:
        """Calculate pairwise similarity matrix"""
        n = len(results)
        similarity = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                if not results[i].generated_code or not results[j].generated_code:
                    continue
                
                sim = self._calculate_codebleu(
                    results[i].generated_code,
                    results[j].generated_code
                )
                similarity[i][j] = sim
                similarity[j][i] = sim
        
        return similarity