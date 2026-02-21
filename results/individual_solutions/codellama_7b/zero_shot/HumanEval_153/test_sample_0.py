"""
Test for AI Generated Solution
Task ID: HumanEval/153
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate('Watashi', ['tEN', 'niNE', 'eIGHt8OKe']) == 'Watashi.eIGHt8OKe'
    assert candidate('Boku123', ['nani', 'NazeDa', 'YEs.WeCaNe', '32145tggg']) == 'Boku123.YEs.WeCaNe'
    assert candidate('__YESIMHERE', ['t', 'eMptY', 'nothing', 'zeR00', 'NuLl__', '123NoooneB321']) == '__YESIMHERE.NuLl__'
    assert candidate('K', ['Ta', 'TAR', 't234An', 'cosSo']) == 'K.TAR'
    assert candidate('__HAHA', ['Tab', '123', '781345', '-_-']) == '__HAHA.123'
    assert candidate('YameRore', ['HhAas', 'okIWILL123', 'WorkOut', 'Fails', '-_-']) == 'YameRore.okIWILL123'
    assert candidate('finNNalLLly', ['Die', 'NowW', 'Wow', 'WoW']) == 'finNNalLLly.WoW'

    # Check some edge cases that are easy to work out by hand.
    assert candidate('_', ['Bb', '91245']) == '_.Bb'
    assert candidate('Sp', ['671235', 'Bb']) == 'Sp.671235'
    
