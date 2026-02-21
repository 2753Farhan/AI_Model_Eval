"""
AI Generated Solution
Task ID: HumanEval/124
Model: codellama:7b
Strategy: zero_shot
Sample ID: 0
Generated: 2026-01-11T00:13:26.296081
"""

def valid_date(date):
    if not date:
        return False
    if not date.count("-") == 2:
        return False
    month, day, year = date.split("-")
    if not month.isdigit() or not day.isdigit() or not year.isdigit():
        return False
    month = int(month)
    day = int(day)
    year = int(year)
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if year < 0 or year > 9999:
        return False
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
        return False
    if month == 2 and day > 29:
        return False
    return True