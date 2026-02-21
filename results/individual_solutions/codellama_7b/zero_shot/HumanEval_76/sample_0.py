"""
AI Generated Solution
Task ID: HumanEval/76
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.230017
"""

def is_simple_power(x, n):
    return x == n ** int(math.log(x, n))

#or
def is_simple_power(x, n):
    return x == n ** (math.log(x) // math.log(n))

#or
from sympy import sympify, Eq

def is_simple_power(x, n):
    expr = sympify(f'{n}**x')
    return Eq(expr, x).rewrite(pow=True) == True