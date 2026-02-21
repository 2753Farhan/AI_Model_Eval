"""
Test for AI Generated Solution
Task ID: HumanEval/32
Model: codellama:7b
"""

def find_zero(xs):
    if len(xs) % 2 == 1 or max(xs[::2]) <= 0:
        return None
    x0 = -max(xs[::2])
    while True:
        y = poly(xs, x0)
        if abs(y) < 1e-6:
            return x0
        x1 = x0 - y / poly(xs, x0)
        if abs(x1 - x0) < 1e-6:
            return x1
        x0 = x1



METADATA = {}


def check(candidate):
    import math
    import random
    rng = random.Random(42)
    import copy
    for _ in range(100):
        ncoeff = 2 * rng.randint(1, 4)
        coeffs = []
        for _ in range(ncoeff):
            coeff = rng.randint(-10, 10)
            if coeff == 0:
                coeff = 1
            coeffs.append(coeff)
        solution = candidate(copy.deepcopy(coeffs))
        assert math.fabs(poly(coeffs, solution)) < 1e-4

