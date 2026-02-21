"""
AI Generated Solution
Task ID: HumanEval/95
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.258038
"""

def check_dict_case(dict):
    if not dict:
        return False
    keys = list(dict.keys())
    if len(set(keys)) != len(keys):
        return False
    if all(isinstance(key, str) and key.islower() for key in keys):
        return True
    elif all(isinstance(key, str) and key.isupper() for key in keys):
        return True
    else:
        return False