"""
AI Generated Solution
Task ID: HumanEval/12
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.112876
"""

def longest(strings: List[str]) -> Optional[str]:
    if not strings:
        return None

    longest_string = ""
    for string in strings:
        if len(string) > len(longest_string):
            longest_string = string

    return longest_string
