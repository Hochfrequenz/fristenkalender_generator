"""
This module can produce a list of calender entries with bdew Fristen
"""

import dataclasses
from calendar import monthrange
from datetime import date

from bdew_datetimes.periods import get_nth_working_day_of_month, get_previous_working_day


@dataclasses.dataclass(unsafe_hash=True)
class FristWithAttributes:
    """
    This class represents a Frist with its attibutes:
    date_of_the_frist = date(y,m,d)
    label = str, where label can be for example '5WT' (5 Werktage des Liefermonats)
    """

    date_of_the_frist: date  # the variable name is longer since date is already defined
    label: str


class FristenkalenderGenerator:
    """
    This class can generate a bdew fristen calender for a given year
    """

    def generate_fristen_list_variable_wt(self, year: int, nth_day: int, label: str) -> list[FristWithAttributes]:
        """
        generate the list of nth_day WT Fristen for a given year
        """

        # the Hochfrequenz Fristenkalender ranges from December of the previous year
        # until the end of January of the following year
        lower_bound = date(year - 1, 12, 1)
        upper_bound = date(year + 1, 2, 1)

        fristen: list[FristWithAttributes] = []

        # oct from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 10, 1))
        if nth_working_day_of_month_date >= lower_bound:
            fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # nov from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 11, 1))
        if nth_working_day_of_month_date >= lower_bound:
            fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # dez from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 12, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year, i_month, 1))
            if nth_working_day_of_month_date < upper_bound:
                fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # jan of next year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year + 1, 1, 1))
        if nth_working_day_of_month_date < upper_bound:
            fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        return fristen

    def generate_fristen_list_lwt(self, year: int) -> list[FristWithAttributes]:
        """
        generate the list of LWT Fristen for a given year
        """

        label = "LWT"
        fristen: list[FristWithAttributes] = []

        def generate_frist(year, month):
            last_day_of_month = monthrange(year, month)[1]
            last_date_of_month = date(year, month, last_day_of_month)
            return FristWithAttributes(get_previous_working_day(last_date_of_month), label)

        # dez last year
        fristen.append(generate_frist(year - 1, 12))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            fristen.append(generate_frist(year, i_month))

        # jan next year
        fristen.append(generate_frist(year + 1, 1))

        return fristen

    def generate_fristen_list_3lwt(self, year: int) -> list[FristWithAttributes]:
        """
        generate the list of 3LWT Fristen for a given year
        """

        label = "3LWT"
        fristen: list[FristWithAttributes] = []

        def generate_frist(year, month):
            last_day_of_month = monthrange(year, month)[1]
            date_dummy = get_previous_working_day(date(year, month, last_day_of_month))
            while last_day_of_month - date_dummy.day < 3:
                date_dummy = get_previous_working_day(date_dummy)
            return date_dummy

        # dez last year
        fristen.append(FristWithAttributes(generate_frist(year - 1, 12), label))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            fristen.append(FristWithAttributes(generate_frist(year, i_month), label))

        # jan next year
        fristen.append(FristWithAttributes(generate_frist(year + 1, 1), label))

        return fristen

    def generate_all_fristen_list(self, year: int) -> list[FristWithAttributes]:
        """
        generate the list of all Fristen for a given year
        """
        fristen: list[FristWithAttributes] = []
        fristen.extend(self.generate_fristen_list_variable_wt(year, 5, "5WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 10, "10WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 12, "12WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 14, "14WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 16, "16WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 17, "17WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 18, "18WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 20, "20WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 21, "21WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 26, "26WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 30, "30WT"))
        fristen.extend(self.generate_fristen_list_variable_wt(year, 42, "42WT"))
        fristen.extend(self.generate_fristen_list_lwt(year))
        fristen.extend(self.generate_fristen_list_3lwt(year))

        return fristen
