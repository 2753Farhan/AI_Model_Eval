# src/utils/code_formatter.py
"""
Centralized code formatting for canonical solutions and test cases
"""

import re
from typing import Optional, List, Dict, Any, Set

class CodeFormatter:
    """Formats incomplete code into complete, executable functions"""
    
    # Common type hints that need imports
    TYPE_HINTS = {
        'List': 'from typing import List',
        'Dict': 'from typing import Dict',
        'Set': 'from typing import Set',
        'Tuple': 'from typing import Tuple',
        'Optional': 'from typing import Optional',
        'Union': 'from typing import Union',
        'Any': 'from typing import Any',
        'Callable': 'from typing import Callable',
        'Iterable': 'from typing import Iterable',
        'Generator': 'from typing import Generator',
        'TypeVar': 'from typing import TypeVar',
        'Generic': 'from typing import Generic',
    }
    
    @staticmethod
    def extract_signature_from_prompt(prompt: str, entry_point: str) -> Optional[str]:
        """Extract function signature from prompt"""
        for line in prompt.split('\n'):
            if line.strip().startswith('def ' + entry_point):
                return line.strip()
        return None
    
    @staticmethod
    def _detect_type_hints(code: str) -> Set[str]:
        """
        Detect which type hints are used in the code
        """
        used_hints = set()
        
        # Pattern to match type hints: : List[int], -> List[int], etc.
        patterns = [
            r':\s*(\w+)\[',  # : List[int]
            r'->\s*(\w+)\[',  # -> List[int]
            r'\)\s*->\s*(\w+)',  # ) -> List
            r'=\s*(\w+)\[',  # = List[int]
            r'Union\[',  # Union[
            r'Optional\[',  # Optional[
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                # Handle nested generics
                if '[' in match:
                    main_type = match.split('[')[0].strip()
                    if main_type in CodeFormatter.TYPE_HINTS:
                        used_hints.add(main_type)
                elif match in CodeFormatter.TYPE_HINTS:
                    used_hints.add(match)
        
        # Also check for standalone type names
        for type_hint in CodeFormatter.TYPE_HINTS:
            # Look for patterns like : List, -> List, etc.
            if re.search(rf':\s*{type_hint}\b', code) or re.search(rf'->\s*{type_hint}\b', code):
                used_hints.add(type_hint)
        
        return used_hints
    
    @staticmethod
    def format_canonical_solution(
        solution: str,
        entry_point: str,
        prompt: str = "",
        signature: Optional[str] = None
    ) -> str:
        """
        Format a canonical solution (function body) into a complete function
        
        Args:
            solution: The function body (may have indentation issues)
            entry_point: The function name
            prompt: The problem prompt (to extract signature)
            signature: Optional pre-extracted signature
        
        Returns:
            Complete, properly formatted function code
        """
        if not solution:
            return ""
        
        # Get signature if not provided
        if not signature:
            signature = CodeFormatter.extract_signature_from_prompt(prompt, entry_point)
        
        if not signature:
            # Fallback signature - use proper typing
            signature = f"def {entry_point}(*args, **kwargs) -> Any:"
        
        # Split solution into lines
        lines = solution.split('\n')
        
        # Find the minimum indentation level (dedent first)
        non_empty_lines = [line for line in lines if line.strip()]
        if non_empty_lines:
            # Find minimum indentation among non-empty lines
            min_indent = min(
                len(line) - len(line.lstrip()) 
                for line in non_empty_lines
            )
            
            # Dedent all lines by the minimum amount
            dedented_lines = []
            for line in lines:
                if line.strip():
                    # Remove the common indentation
                    if len(line) > min_indent:
                        dedented_lines.append(line[min_indent:])
                    else:
                        dedented_lines.append(line.lstrip())
                else:
                    dedented_lines.append('')  # Keep empty lines
        else:
            dedented_lines = lines
        
        # Now add proper 4-space indentation
        indented_lines = ['    ' + line if line.strip() else line for line in dedented_lines]
        
        # Combine signature with formatted body
        complete_code = signature + '\n' + '\n'.join(indented_lines)
        
        # Add necessary imports based on code content
        used_hints = CodeFormatter._detect_type_hints(complete_code)
        
        # Always include basic typing imports if any type hints are used
        if used_hints:
            imports = ["from typing import " + ", ".join(sorted(used_hints))]
            complete_code = '\n'.join(imports) + '\n\n' + complete_code
        elif 'import' not in complete_code and any(hint in complete_code for hint in CodeFormatter.TYPE_HINTS):
            # Fallback: import common types if they appear but weren't detected
            imports = ["from typing import List, Dict, Optional, Union, Any, Tuple, Set"]
            complete_code = '\n'.join(imports) + '\n\n' + complete_code
        
        return complete_code
    
    @staticmethod
    def clean_model_output(raw_code: str) -> str:
        """
        Clean raw model output (remove markdown, tags, etc.)
        
        Args:
            raw_code: Raw output from model
        
        Returns:
            Cleaned code
        """
        if not raw_code:
            return ""
        
        # Remove [PYTHON] tags
        code = raw_code.replace('[PYTHON]', '').replace('[/PYTHON]', '')
        
        # Remove markdown code blocks
        code_block_patterns = [
            (r'```python\n(.*?)\n```', re.DOTALL),
            (r'```\n(.*?)\n```', re.DOTALL),
            (r'```(.*?)```', re.DOTALL),
        ]
        
        for pattern, flags in code_block_patterns:
            match = re.search(pattern, code, flags)
            if match:
                code = match.group(1)
                break
        
        # Remove any explanatory text before the function
        lines = code.split('\n')
        code_lines = []
        found_def = False
        in_function = False
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Check for function definition
            if stripped.startswith('def '):
                found_def = True
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                code_lines.append(line)
            elif found_def and in_function:
                # Check if we're still in the function (based on indentation)
                current_indent = len(line) - len(line.lstrip())
                if stripped and current_indent > indent_level:
                    code_lines.append(line)
                elif not stripped:
                    code_lines.append(line)  # Keep empty lines
                else:
                    # Found line with less indentation - function ended
                    in_function = False
                    # Don't break - we might have multiple functions
        
        if code_lines:
            code = '\n'.join(code_lines)
        
        # Add missing imports for common type hints
        if 'List[' in code and 'from typing import' not in code:
            used_hints = CodeFormatter._detect_type_hints(code)
            if used_hints:
                imports = "from typing import " + ", ".join(sorted(used_hints))
                code = imports + '\n\n' + code
        
        return code.strip()
    
    @staticmethod
    def prepare_for_execution(
        code: str,
        entry_point: Optional[str] = None,
        prompt: Optional[str] = None,
        is_canonical: bool = False
    ) -> str:
        """
        Prepare any code for execution in the sandbox
        
        Args:
            code: The code to prepare
            entry_point: Function name (required for canonical solutions)
            prompt: Original problem prompt (for extracting signature)
            is_canonical: Whether this is a canonical solution (needs formatting)
        
        Returns:
            Code ready for execution
        """
        if not code:
            return ""
        
        if is_canonical and entry_point:
            # This is a canonical solution - needs formatting
            return CodeFormatter.format_canonical_solution(code, entry_point, prompt or "")
        else:
            # This is model output - just clean it
            return CodeFormatter.clean_model_output(code)
    
    @staticmethod
    def prepare_test_cases_for_execution(
        test_cases: List[Dict[str, Any]],
        entry_point: str
    ) -> List[Dict[str, Any]]:
        """
        Prepare test cases for execution by replacing 'candidate'
        
        Args:
            test_cases: Raw test cases from dataset
            entry_point: Actual function name
        
        Returns:
            Test cases ready for execution
        """
        formatted = []
        for test in test_cases:
            if isinstance(test, dict):
                formatted_test = {}
                for key, value in test.items():
                    if key == 'assertion' and isinstance(value, str):
                        # Replace 'candidate' with actual function name
                        formatted_test[key] = value.replace('candidate', entry_point)
                    else:
                        formatted_test[key] = value
                formatted.append(formatted_test)
            else:
                formatted.append(test)
        return formatted
    
    @staticmethod
    def add_typing_imports(code: str) -> str:
        """
        Add necessary typing imports to code if they're missing
        
        Args:
            code: The code to check
        
        Returns:
            Code with typing imports added if needed
        """
        if 'from typing import' in code or 'import typing' in code:
            return code
        
        used_hints = CodeFormatter._detect_type_hints(code)
        if used_hints:
            imports = "from typing import " + ", ".join(sorted(used_hints))
            return imports + '\n\n' + code
        
        return code