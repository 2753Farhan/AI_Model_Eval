"""
AI Generated Solution
Task ID: HumanEval/81
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.238012
"""

def numerical_letter_grade(grades):
    letter_grades = []
    for gpa in grades:
        if gpa >= 4.0:
            letter_grade = 'A+'
        elif gpa >= 3.7:
            letter_grade = 'A'
        elif gpa >= 3.3:
            letter_grade = 'A-'
        elif gpa >= 3.0:
            letter_grade = 'B+'
        elif gpa >= 2.7:
            letter_grade = 'B'
        elif gpa >= 2.3:
            letter_grade = 'B-'
        elif gpa >= 2.0:
            letter_grade = 'C+'
        elif gpa >= 1.7:
            letter_grade = 'C'
        elif gpa >= 1.3:
            letter_grade = 'C-'
        elif gpa >= 1.0:
            letter_grade = 'D+'
        elif gpa >= 0.7:
            letter_grade = 'D'
        else:
            letter_grade = 'E'
        letter_grades.append(letter_grade)
    return letter_grades