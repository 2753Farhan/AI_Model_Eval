"""
AI Generated Solution
Task ID: HumanEval/72
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.225498
"""

def will_it_fly(q,w):
    if len(q) == 0:
        return False
    if q[0] != q[-1]:
        return False
    total = 0
    for i in range(len(q)):
        total += q[i]
    return total <= w and total == sum(q)

#or using built-in sum function:
def will_it_fly(q,w):
    if len(q) == 0:
        return False
    if q[0] != q[-1]:
        return False
    return sum(q) <= w and sum(q) == sum(q)

#or using built-in sum function and palindrome check:
def will_it_fly(q,w):
    return len(q) > 0 and q == q[::-1] and sum(q) <= w