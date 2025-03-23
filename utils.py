# utils.py

def implied_probability(odds):
    try:
        return round(1 / odds, 4)
    except ZeroDivisionError:
        return 0
