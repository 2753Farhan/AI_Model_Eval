"""
AI Generated Solution
Task ID: HumanEval/162
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.351180
"""

def string_to_md5(text):
    if text == "":
        return None
    else:
        import hashlib
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()