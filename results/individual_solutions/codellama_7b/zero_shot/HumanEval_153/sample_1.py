"""
AI Generated Solution
Task ID: HumanEval/153
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.338668
"""

def strongest_extension(class_name, extensions):
    strengths = []
    for extension in extensions:
        cap = sum(1 for c in extension if c.isupper())
        sm = sum(1 for c in extension if c.islower())
        strengths.append(cap - sm)
    strongest_index = strengths.index(max(strengths))
    return f"{class_name}.{extensions[strongest_index]}"