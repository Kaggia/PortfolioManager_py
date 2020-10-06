#date.py
#Classe per la descrizione custom delle date
from datetime import date

def get_day_of_week(_date):
    d = date(_date.y, _date.m, _date.d)
    print("Day of week is: ", d.weekday())
    return d.weekday()
def reset_to_monday(_date, _date_as_value):
    DAY_AS_MINUTES = 1440
    d = date(_date.y, _date.m, _date.d)
    current_day = d.weekday()
    minutes_to_subtract = DAY_AS_MINUTES * current_day

    return _date_as_value - minutes_to_subtract

class Date:
    def __init__(self, day, month, year):
        self.d = int(day)
        self.m = int(month)
        self.y = int(year)