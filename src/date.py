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
class CompleteDate:
    def __init__(self, day, month, year, hours, minutes):
        self.d = int(day)
        self.m = int(month)
        self.y = int(year)
        self.h = int(hours)
        self.mins = int(minutes)
        self.internal_date = self.__convert_date_to_internalDate__(self.m, self.d, self.y, self.h, self.mins)
    def __convert_date_to_internalDate__(self, _month, _day, _year, _hour, _minute):
        day_value = (int(_day) - 1 ) * 1440
        month_value = (int(_month) - 1 ) * 43800
        year_value = (int(_year) - 2000 ) * 524160
        hour_value = int(_hour) * 60
        minute_value = int(_minute)
        sum_of_minutes = day_value + month_value + year_value + hour_value + minute_value

        return sum_of_minutes