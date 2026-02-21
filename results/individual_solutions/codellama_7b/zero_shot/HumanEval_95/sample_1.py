"""
AI Generated Solution
Task ID: HumanEval/95
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.259038
"""

def check_dict_case(my_dict):
    if not my_dict:
        return False
    are_all_keys_lower = all(key.islower() for key in my_dict.keys())
    are_all_keys_upper = all(key.isupper() for key in my_dict.keys())
    return are_all_keys_lower or are_all_keys_upper