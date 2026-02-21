"""
Test for AI Generated Solution
Task ID: HumanEval/135
Model: codellama:7b
"""

def can_arrange(arr):
    for i in range(len(arr)-1):
        if arr[i] >= arr[i+1]:
            return -1
    return len(arr)-1

# Test case 1:
print(can_arrange([1,2,4,3,5])) # Output: 3
# Test case 2:
print(can_arrange([1,2,3])) # Output: -1

def check(candidate):

    # Check some simple cases
    assert candidate([1,2,4,3,5])==3
    assert candidate([1,2,4,5])==-1
    assert candidate([1,4,2,5,6,7,8,9,10])==2
    assert candidate([4,8,5,7,3])==4

    # Check some edge cases that are easy to work out by hand.
    assert candidate([])==-1

