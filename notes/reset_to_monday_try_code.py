from datetime import date

#date.py
#Classe per la descrizione custom delle date
def get_day_of_week(_date):
    d = date(_date.y, _date.m, _date.d)
    print("Day of week is: ", d.weekday())
    return d.weekday()
def reset_to_monday(_date, _date_as_value):
    print("Not resetted day: ", _date_as_value)
    DAY_AS_MINUTES = 1440
    d = date(_date.y, _date.m, _date.d)
    current_day = d.weekday()
    minutes_to_subtract = DAY_AS_MINUTES * current_day

    return _date_as_value - minutes_to_subtract

def __convert_date_to_internalDate__(_month, _day, _year, _hour, _minute):
        day_value = (int(_day) - 1 ) * 1440
        month_value = (int(_month) - 1 ) * 43800
        year_value = (int(_year) - 2000 ) * 524160
        hour_value = int(_hour) * 60
        minute_value = int(_minute)
        sum_of_minutes = day_value + month_value + year_value + hour_value + minute_value

        return sum_of_minutes

class Date:
    def __init__(self, day, month, year):
        self.d = day
        self.m = month
        self.y = year

d = Date(29, 9, 2020)
rd = Date(28, 9, 2020)

print("Resetted day to monday: ", reset_to_monday(d, __convert_date_to_internalDate__(d.m,d.d, d.y, 0, 0)))
print("Monday: ", __convert_date_to_internalDate__(9, 28, 2020, 0, 0))
print("Difference: ", str(reset_to_monday(d, __convert_date_to_internalDate__(d.m,d.d, d.y, 0, 0)) - __convert_date_to_internalDate__(9, 28, 2020, 0, 0)))