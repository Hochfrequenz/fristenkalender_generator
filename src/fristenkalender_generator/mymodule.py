"""
This a docstring for the module.
"""

from bdew_datetimes.periods import get_nth_working_day_of_month, get_previous_working_day
from calendar import monthrange
from datetime import date


class Fristenkalender_generator:
    """
    This class is made to create a bedw fristen kalender for a given year
    """

    def __init__(self):
        """
        Initialize for the sake of initializing
        """

    def generate_fristen_liste_variable_WT(self, year: int, nth_day: int, fristen_type: str) -> list:
        """
        generate the list of nth_day WT Fristen for a given year
        """

        fristen_list = []

        # oct from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 10, 1))
        if nth_working_day_of_month_date >= date(year - 1, 12, 1):
            fristen_list.append((fristen_type, nth_working_day_of_month_date))

        # nov from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 11, 1))
        if nth_working_day_of_month_date >= date(year - 1, 12, 1):
            fristen_list.append((fristen_type, nth_working_day_of_month_date))

        # dez from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 12, 1))
        fristen_list.append((fristen_type, nth_working_day_of_month_date))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year, i_Month, 1))
            if nth_working_day_of_month_date < date(year + 1, 2, 1):
                fristen_list.append((fristen_type, nth_working_day_of_month_date))

        # jan of next year
        nth_working_day_of_month_date = get_nth_working_day_of_month(
            nth_day, start=date(year + 1, 12, 1)
        )  # dez form last year
        if nth_working_day_of_month_date < date(year + 1, 2, 1):
            fristen_list.append((fristen_type, nth_working_day_of_month_date))

        return fristen_list

    def generate_fristen_liste_LWT(self, year: int) -> list:
        """
        generate the list of LWT Fristen for a given year
        """

        fristen_type = "LWT"
        fristen_list = []

        # dez last year
        last_day_of_Month = monthrange(year, 12)[1]
        last_date_of_Month = date(year - 1, 12, last_day_of_Month)
        fristen_list.append((fristen_type, get_previous_working_day(last_date_of_Month)))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            last_day_of_Month = monthrange(year, i_Month)[1]
            last_date_of_Month = date(year - 1, 12, last_day_of_Month)
            fristen_list.append((fristen_type, get_previous_working_day(last_date_of_Month)))

        # jan next year
        last_day_of_Month = monthrange(year, 1)[1]
        last_date_of_Month = date(year + 1, 1, last_day_of_Month)
        fristen_list.append((fristen_type, get_previous_working_day(last_date_of_Month)))

        return fristen_list

    def generate_fristen_liste_3LWT(self, year: int) -> list:
        """
        generate the list of LWT Fristen for a given year
        """

        fristen_type = "3LWT"
        fristen_list = []

        # dez last year
        last_day_of_Month = monthrange(year - 1, 12)[1]
        date_dummy = get_previous_working_day(date(year - 1, 12, last_day_of_Month))
        while last_day_of_Month - date_dummy.day < 3:
            date_dummy = get_previous_working_day(date_dummy)
        fristen_list.append((fristen_type, date_dummy))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            last_day_of_Month = monthrange(year, i_Month)[1]
            last_date_of_Month = date(year, i_Month, last_day_of_Month)
            date_dummy = date(year, i_Month, last_day_of_Month)
            date_dummy = get_previous_working_day(date_dummy)
            while last_day_of_Month - date_dummy.day < 3:
                date_dummy = get_previous_working_day(date_dummy)
            fristen_list.append((fristen_type, date_dummy))

        # jan next year
        last_day_of_Month = monthrange(year + 1, 1)[1]
        date_dummy = date(year + 1, 1, last_day_of_Month)
        date_dummy = get_previous_working_day(date_dummy)
        while last_day_of_Month - date_dummy.day < 3:
            date_dummy = get_previous_working_day(date_dummy)
        fristen_list.append((fristen_type, date_dummy))

        return fristen_list

    def generate_fristen_df(self, year: int) -> list:
        """
        generate the list of all Fristen for a given year
        """
        fristen_list = []
        fristen_list.append(generate_fristen_liste_variable_WT(year, 5, "5WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 10, "10WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 12, "12WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 14, "14WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 16, "16WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 17, "17WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 18, "18WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 20, "20WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 21, "21WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 26, "26WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 30, "30WT"))
        fristen_list.append(generate_fristen_liste_variable_WT(year, 42, "42WT"))
        fristen_list.append(generate_fristen_liste_LWT(year))
        fristen_list.append(generate_fristen_liste_3LWT(year))

        return fristen_list


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
