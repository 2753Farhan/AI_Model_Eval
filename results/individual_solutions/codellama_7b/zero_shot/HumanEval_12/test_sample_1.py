"""
Test for AI Generated Solution
Task ID: HumanEval/12
Model: codellama:7b
"""

def longest(strings: List[str]) -> Optional[str]:
    if not strings:
        return None

    longest_string = ""
    for string in strings:
        if len(string) > len(longest_string):
            longest_string = string

    return longest_string




METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == None
    assert candidate(['x', 'y', 'z']) == 'x'
    assert candidate(['x', 'yyy', 'zzzz', 'www', 'kkkk', 'abc']) == 'zzzz'
