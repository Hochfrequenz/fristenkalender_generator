"""
This module can produce a list of calender entries with bdew Fristen
"""

from bdew_datetimes.periods import get_nth_working_day_of_month, get_previous_working_day
from calendar import monthrange
from datetime import date, datetime
import dataclasses


@dataclasses.dataclass
class Frist_with_attributes:
    """
    This class represents a Frist with its attibutes: date_of_the_frist = date(y,m,d) and type_of_the_frist = '...'
    """

    date_of_the_frist: date
    type_of_the_frist: str


@dataclasses.dataclass
class Date_with_all_its_fristen:
    """
    This calss represents a day with all its Fristen
    """

    date_of_the_day: datetime
    list_of_fristen: list


class Fristenkalender_generator:
    """
    This class is made to create a bedw fristen kalender for a given year
    """

    def __init__(self):
        """
        Initialize for the sake of initializing
        """

    def generate_fristen_list_variable_WT(self, year: int, nth_day: int, fristen_type: str) -> list:
        """
        generate the list of nth_day WT Fristen for a given year
        """

        fristen_list = []

        # oct from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 10, 1))
        if nth_working_day_of_month_date >= date(year - 1, 12, 1):
            fristen_list.append(Frist_with_attributes(nth_working_day_of_month_date, fristen_type))

        # nov from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 11, 1))
        if nth_working_day_of_month_date >= date(year - 1, 12, 1):
            fristen_list.append(Frist_with_attributes(nth_working_day_of_month_date, fristen_type))

        # dez from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 12, 1))
        fristen_list.append(Frist_with_attributes(nth_working_day_of_month_date, fristen_type))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year, i_Month, 1))
            if nth_working_day_of_month_date < date(year + 1, 2, 1):
                fristen_list.append(Frist_with_attributes(nth_working_day_of_month_date, fristen_type))

        # jan of next year
        nth_working_day_of_month_date = get_nth_working_day_of_month(
            nth_day, start=date(year + 1, 12, 1)
        )  # dez form last year
        if nth_working_day_of_month_date < date(year + 1, 2, 1):
            fristen_list.append(Frist_with_attributes(nth_working_day_of_month_date, fristen_type))

        return fristen_list

    def generate_fristen_list_LWT(self, year: int) -> list:
        """
        generate the list of LWT Fristen for a given year
        """

        fristen_type = "LWT"
        fristen_list = []

        # dez last year
        last_day_of_Month = monthrange(year, 12)[1]
        last_date_of_Month = date(year - 1, 12, last_day_of_Month)
        fristen_list.append(Frist_with_attributes(get_previous_working_day(last_date_of_Month), fristen_type))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            last_day_of_Month = monthrange(year, i_Month)[1]
            last_date_of_Month = date(year - 1, 12, last_day_of_Month)
            fristen_list.append(Frist_with_attributes(get_previous_working_day(last_date_of_Month), fristen_type))

        # jan next year
        last_day_of_Month = monthrange(year, 1)[1]
        last_date_of_Month = date(year + 1, 1, last_day_of_Month)
        fristen_list.append(Frist_with_attributes(get_previous_working_day(last_date_of_Month), fristen_type))

        return fristen_list

    def generate_fristen_list_3LWT(self, year: int) -> list:
        """
        generate the list of 3LWT Fristen for a given year
        """

        fristen_type = "3LWT"
        fristen_list = []

        # dez last year
        last_day_of_Month = monthrange(year - 1, 12)[1]
        date_dummy = get_previous_working_day(date(year - 1, 12, last_day_of_Month))
        while last_day_of_Month - date_dummy.day < 3:
            date_dummy = get_previous_working_day(date_dummy)
        fristen_list.append(Frist_with_attributes(date_dummy, fristen_type))

        # this year
        n_Months = 12
        for i_Month in range(1, n_Months + 1):
            last_day_of_Month = monthrange(year, i_Month)[1]
            last_date_of_Month = date(year, i_Month, last_day_of_Month)
            date_dummy = get_previous_working_day(date(year, i_Month, last_day_of_Month))
            while last_day_of_Month - date_dummy.day < 3:
                date_dummy = get_previous_working_day(date_dummy)
            fristen_list.append(Frist_with_attributes(date_dummy, fristen_type))

        # jan next year
        last_day_of_Month = monthrange(year + 1, 1)[1]
        date_dummy = get_previous_working_day(date(year + 1, 1, last_day_of_Month))
        while last_day_of_Month - date_dummy.day < 3:
            date_dummy = get_previous_working_day(date_dummy)
        fristen_list.append(Frist_with_attributes(date_dummy, fristen_type))

        return fristen_list

    def generate_all_fristen_list(self, year: int) -> list:
        """
        generate the list of all Fristen for a given year
        """
        fristen_list = []
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 5, "5WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 10, "10WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 12, "12WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 14, "14WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 16, "16WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 17, "17WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 18, "18WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 20, "20WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 21, "21WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 26, "26WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 30, "30WT"))
        fristen_list.extend(self.generate_fristen_list_variable_WT(year, 42, "42WT"))
        fristen_list.extend(self.generate_fristen_list_LWT(year))
        fristen_list.extend(self.generate_fristen_list_3LWT(year))

        return fristen_list
