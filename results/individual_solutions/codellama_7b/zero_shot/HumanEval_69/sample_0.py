"""
AI Generated Solution
Task ID: HumanEval/69
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.219492
"""

def search(lst):
    freq = {}
    for i in lst:
        if i not in freq:
            freq[i] = 1
        else:
            freq[i] += 1
    
    for i in freq:
        if freq[i] >= i and i > 0:
            return i
    
    return -1