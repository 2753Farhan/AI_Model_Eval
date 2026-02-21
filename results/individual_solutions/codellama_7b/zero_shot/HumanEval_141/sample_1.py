"""
AI Generated Solution
Task ID: HumanEval/141
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.321649
"""

def file_name_check(file_name):
    if len(file_name) > 3:
        return "No"
    if file_name.count(".") != 1:
        return "No"
    if not file_name[0].isalpha():
        return "No"
    extension = file_name.split(".")[-1]
    if extension not in ["txt", "exe", "dll"]:
        return "No"
    return "Yes"