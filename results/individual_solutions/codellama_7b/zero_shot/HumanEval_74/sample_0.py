"""
AI Generated Solution
Task ID: HumanEval/74
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.227496
"""

def total_match(list1, list2):
    count1 = sum([len(i) for i in list1])
    count2 = sum([len(i) for i in list2])
    if count1 < count2:
        return list1
    elif count1 > count2:
        return list2
    else:
        return list1