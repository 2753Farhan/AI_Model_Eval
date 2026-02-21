"""
AI Generated Solution
Task ID: HumanEval/58
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.202467
"""

def common(list1, list2):
    return sorted(set(list1).intersection(set(list2)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()