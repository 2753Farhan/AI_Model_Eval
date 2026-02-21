"""
AI Generated Solution
Task ID: HumanEval/137
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.315646
"""

def compare_one(a, b):
    if a == b:
        return None
    elif isinstance(a, int) and isinstance(b, float):
        return b
    elif isinstance(a, str) and isinstance(b, float):
        # check if the floating point is . or ,
        if "." in a:
            a = float(a.replace(",", "."))
        else:
            b = float(b.replace(",", "."))
        if a > b:
            return a
        else:
            return b
    elif isinstance(a, int) and isinstance(b, str):
        # check if the floating point is . or ,
        if "." in b:
            b = float(b.replace(",", "."))
        else:
            a = float(a.replace(",", "."))
        if a > b:
            return a
        else:
            return b
    else:
        if a > b:
            return a
        else:
            return b
