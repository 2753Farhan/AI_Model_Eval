"""
Test for AI Generated Solution
Task ID: HumanEval/124
Model: codellama:7b
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

def check(candidate):

    # Check some simple cases
    assert candidate('03-11-2000') == True

    assert candidate('15-01-2012') == False

    assert candidate('04-0-2040') == False

    assert candidate('06-04-2020') == True

    assert candidate('01-01-2007') == True

    assert candidate('03-32-2011') == False

    assert candidate('') == False

    assert candidate('04-31-3000') == False

    assert candidate('06-06-2005') == True

    assert candidate('21-31-2000') == False

    assert candidate('04-12-2003') == True

    assert candidate('04122003') == False

    assert candidate('20030412') == False

    assert candidate('2003-04') == False

    assert candidate('2003-04-12') == False

    assert candidate('04-2003') == False
