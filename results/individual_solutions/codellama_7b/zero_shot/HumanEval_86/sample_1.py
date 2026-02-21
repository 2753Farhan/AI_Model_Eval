"""
AI Generated Solution
Task ID: HumanEval/86
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.245525
"""

def anti_shuffle(s):
    # Split the string into a list of words using split()
    words = s.split()
    
    # Iterate through the words and sort them alphabetically
    for i in range(len(words)):
        words[i] = ''.join(sorted(words[i]))
    
    # Join the sorted words back into a string
    return ' '.join(words)