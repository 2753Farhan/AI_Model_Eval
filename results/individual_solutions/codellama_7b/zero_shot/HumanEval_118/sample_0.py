"""
AI Generated Solution
Task ID: HumanEval/118
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.288568
"""

def get_closest_vowel(word):
    vowels = ['a', 'e', 'i', 'o', 'u']
    for i in range(len(word)-1, -1, -1):
        if word[i] in vowels:
            if i < len(word)-1 and word[i+1] not in vowels:
                return word[i]
            elif i > 0 and word[i-1] not in vowels:
                return word[i]
    return ''


# Test cases:
print(get_closest_vowel("yogurt")) # u
print(get_closest_vowel("FULL")) # U
print(get_closest_vowel("quick")) # ""
print(get_closest_vowel("ab")) # ""