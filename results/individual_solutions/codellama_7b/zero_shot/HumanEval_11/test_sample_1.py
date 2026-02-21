"""
Test for AI Generated Solution
Task ID: HumanEval/11
Model: codellama:7b
"""

def string_xor(a, b):
    result = []
    for i, j in zip(a, b):
        if i == j:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('111000', '101010') == '010010'
    assert candidate('1', '1') == '0'
    assert candidate('0101', '0000') == '0101'
