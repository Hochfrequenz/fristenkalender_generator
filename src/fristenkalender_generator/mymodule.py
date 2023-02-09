"""
This a docstring for the module.
"""

from datetime import date
from bdew_datetimes.periods import get_nth_working_day_of_month, MonthType
from bdew_datetimes import create_bdew_calendar
#from calendar import monthrange
import pandas as pd

class Fristenkalender_generator:
    """
    This is a doctring for the class
    """

    def __init__(self):
        """
        Initialize for the sake of initializing
        """

    def generate_fristen_liste_variable_WT(self, year, nth_day, fristen_type):
        """
        generate the list of 5WT Fristen for a given year
        """

        df_fristen = pd.DataFrame()

        i_fristen = 0

        # oct from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day,start=date(year - 1, 10, 1))
        if nth_working_day_of_month_date >= date(year - 1, 12, 1):
            df_fristen.loc[i_fristen, ('type', 'date')] = [fristen_type, nth_working_day_of_month_date]
            i_fristen += 1

        # nov from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day,start=date(year - 1, 11, 1))
        if nth_working_day_of_month_date >= date(year-1,12,1):
            df_fristen.loc[i_fristen, ('type', 'date')] = [fristen_type, nth_working_day_of_month_date]
            i_fristen += 1

        # dez from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day,start=date(year - 1, 12, 1))
        df_fristen.loc[i_fristen,('type', 'date')] = [fristen_type, nth_working_day_of_month_date]
        i_fristen += 1

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day,start=date(year, i_Month, 1))
            if nth_working_day_of_month_date < date(year + 1, 2, 1):
                df_fristen.loc[i_fristen, ('type', 'date')] = [fristen_type, nth_working_day_of_month_date]
                i_fristen += 1

        # jan of next year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year + 1, 12, 1))  # dez form last year
        if nth_working_day_of_month_date < date(year + 1, 2, 1):
            df_fristen.loc[i_fristen, ('type', 'date')] = [fristen_type, nth_working_day_of_month_date]

        return df_fristen


    def generate_fristen_df(self, year):
        df_fristen = pd.DataFrame()
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 5, '5WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 10, '10WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 12, '12WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 14, '14WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 16, '16WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 17, '17WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 18, '18WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 20, '20WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 21, '21WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 26, '26WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 30, '30WT'), ignore_index=True)
        df_fristen = df_fristen.append(generate_fristen_liste_variable_WT(2023, 42, '42WT'), ignore_index=True)
        return df_fristen






#Fristenkalender_generator().kalender(2022)
#

# Frinstenkalender_generator.kalender(year)


class MyClass:  # pylint: disable=too-few-public-methods
    """
    This is a docstring for the class.
    """

    def __init__(self):
        """
        Initialize for the sake of initializing
        """
        self.my_instance_var: str = "abc"

    def do_something(self) -> str:
        """
        Actually does nothing.
        :return: the value of an instance variable
        """
        # this is a super long line with: 100 < line length <= 120 to demonstrate the purpose of pyproject.toml
        return self.my_instance_var
