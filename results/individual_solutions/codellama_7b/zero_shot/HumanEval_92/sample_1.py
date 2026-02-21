"""
AI Generated Solution
Task ID: HumanEval/92
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.255038
"""

def any_int(x, y, z):
    if not x.is_integer() or not y.is_integer() or not z.is_integer():
        return False
    if x + y == z:
        return True
    elif y + z == x:
        return True
    elif z + x == y:
        return True
    else:
        return False