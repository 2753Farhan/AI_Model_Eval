"""
AI Generated Solution
Task ID: HumanEval/141
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.321649
"""

def file_name_check(file_name):
    """
    Args:
        file_name (str): the file name to check
    Returns:
        (bool): True if the file name is valid, False otherwise
    """
    # check if the file name contains more than three digits
    if len(re.findall(r'\d', file_name)) > 3:
        return False
    
    # check if the file name contains a dot and it is not the first character
    if file_name.count('.') != 1 or file_name[0] == '.':
        return False
    
    # check if the substring before the dot starts with a letter
    if not re.match(r'^[a-zA-Z]', file_name[:file_name.index('.'")]):
        return False
    
    # check if the substring after the dot is one of ['txt', 'exe', 'dll']
    extension = file_name[file_name.index('.') + 1:]
    if extension not in ['txt', 'exe', 'dll']:
        return False
    
    return True