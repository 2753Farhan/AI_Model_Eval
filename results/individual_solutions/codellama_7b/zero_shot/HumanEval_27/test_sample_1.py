"""
Test for AI Generated Solution
Task ID: HumanEval/27
Model: codellama:7b
"""

def flip_case(string):
    return string.swapcase()



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == ''
    assert candidate('Hello!') == 'hELLO!'
    assert candidate('These violent delights have violent ends') == 'tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS'
