"""
This module can produce a list of calender entries with bdew Fristen
"""

import dataclasses
from calendar import monthrange
from datetime import date, timedelta

from bdew_datetimes.periods import get_nth_working_day_of_month, get_previous_working_day


@dataclasses.dataclass(unsafe_hash=True)
class FristWithAttributes:
    """
    This class represents a Frist with its attibutes
    """

    date: date  #: = date(y,m,d)
    label: str  #: can be for exmaple '5WT' (5 Werktage des Liefermonats)


class FristenkalenderGenerator:
    """
    This class can generate a bdew fristen calender for a given year
    """

    def generate_fristen_list_variable_wt(self, year: int, nth_day: int, label: str) -> list[FristWithAttributes]:
        """
        Generate the list of fristen for a given year that are on the nth WT (Werktag) of each month of the calender
        """

        fristen: list[FristWithAttributes] = []

        # oct from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 10, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # nov from last year, only if relevant for the current year's calender
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 11, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # dez from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 12, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year, i_month, 1))
            fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # jan of next year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year + 1, 1, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # the Hochfrequenz Fristenkalender ranges from December of the previous year
        # until the end of January of the following year
        lower_bound = date(year - 1, 12, 1)
        upper_bound = date(year + 1, 2, 1)
        fristen_filtered = [frist for frist in fristen if lower_bound <= frist.date < upper_bound]

        return fristen_filtered

    def generate_fristen_list_variable_lwt(self, year: int, nth_day: int, label: str) -> list[FristWithAttributes]:
        """
        Generate the list of fristen for a given year that are on the nth LWT (letzer Werktag)
        of each month of the calender
        LWT are counted back into the month starting from the last day of the month.
        The last day of the month is counted irrespective if it is a wt or not.
        """

        fristen: list[FristWithAttributes] = []

        def generate_lwt_frist(year, month: int) -> FristWithAttributes:
            last_day_of_month = monthrange(year, month)[1]
            last_date_of_month = date(year, month, last_day_of_month)
            first_day_of_next_month = last_date_of_month + timedelta(days=1)
            date_dummy = get_previous_working_day(first_day_of_next_month)
            # the last day of the month counts, regardless if its a wt or not
            i_relevant_days = last_day_of_month - date_dummy.day
            while i_relevant_days < nth_day:
                date_dummy = get_previous_working_day(date_dummy)
                i_relevant_days += 1

            return FristWithAttributes(date_dummy, label)

        # dez last year
        fristen.append(generate_lwt_frist(year - 1, 12))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            fristen.append(generate_lwt_frist(year, i_month))

        # jan next year
        fristen.append(generate_lwt_frist(year + 1, 1))

        return fristen

    def generate_all_fristen(self, year: int) -> list[FristWithAttributes]:
        """
        Generate the list of all Fristen in the calender for a given year
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
        fristen.extend(self.generate_fristen_list_variable_lwt(year, 0, "LWT"))
        fristen.extend(self.generate_fristen_list_variable_lwt(year, 3, "3LWT"))

        return fristen

    def generate_specific_fristen(self, year: int, days_and_labels: list[tuple[int, str]]) -> list[FristWithAttributes]:
        """
        Generate the list of Fristen in the calender for a given year for a given set of Fristen
        The specification of the Fristen is for example: days_and_labels = [(5, '5WT'), (3, 'LWT), ...]
        """

        fristen = []
        for days, label in days_and_labels:
            if label[-3:] == "LWT":
                fristen += self.generate_fristen_list_variable_lwt(year, days, label)
            else:
                fristen += self.generate_fristen_list_variable_wt(year, days, label)

        return fristen
