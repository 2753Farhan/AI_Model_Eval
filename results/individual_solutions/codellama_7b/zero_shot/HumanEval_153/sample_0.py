"""
AI Generated Solution
Task ID: HumanEval/153
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.338668
"""

def strongest_extension(class_name, extensions):
    # Initialize a variable to store the strongest extension
    strongest = ""
    # Calculate the strength of each extension
    for extension in extensions:
        cap = sum(1 for c in extension if c.isupper())
        sm = sum(1 for c in extension if c.islower())
        strength = cap - sm
        # If this is the first extension, set the strongest to it
        if strongest == "":
            strongest = extension
        # If this extension has a higher strength, set it as the strongest
        elif strength > get_strength(strongest):
            strongest = extension
    # Return the class name with the strongest extension
    return class_name + "." + strongest

def get_strength(extension):
    cap = sum(1 for c in extension if c.isupper())
    sm = sum(1 for c in extension if c.islower())
    return cap - sm