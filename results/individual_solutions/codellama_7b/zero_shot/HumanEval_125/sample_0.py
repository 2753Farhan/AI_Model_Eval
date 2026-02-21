"""
AI Generated Solution
Task ID: HumanEval/125
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.297614
"""

def split_words(txt):
    # Check if the string contains any whitespaces
    if ' ' in txt or '\t' in txt:
        return txt.split()
    # If not, check if it contains any commas
    elif ',' in txt:
        return [word for word in txt.split(',') if word]
    # If not, return the number of lower-case letters with odd order in the alphabet
    else:
        count = 0
        for char in txt:
            if char.islower():
                count += (ord(char) - ord('a')) % 2 + 1
        return count
