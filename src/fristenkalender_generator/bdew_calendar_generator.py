"""
This module can produce a list of calendar entries with bdew Fristen
"""

import dataclasses
import os
from calendar import monthrange
from datetime import date, datetime, timedelta

from bdew_datetimes.periods import get_nth_working_day_of_month, get_previous_working_day
from icalendar import Calendar, Event  # type: ignore[import]

from pathlib import Path

@dataclasses.dataclass(unsafe_hash=True)
class FristWithAttributes:
    """
    This class represents a Frist with its attibutes
    """

    date: date  #: = date(y,m,d)
    label: str  #: can be for exmaple '5WT' (5 Werktage des Liefermonats)


class FristenkalenderGenerator:
    """
    This class can generate a bdew fristen calendar for a given year
    """

    def generate_all_fristen_for_given_wt(self, year: int, nth_day: int, label: str) -> list[FristWithAttributes]:
        """
        Generate the list of fristen for a given year that are on the nth WT (Werktag) of each month of the calendar
        """

        fristen: list[FristWithAttributes] = []

        # some fristen starting in Oct/Nov/Dec of the previous year might be relevant
        # we first add them all to the result list and later on remove those entries
        # that are not relevant

        # oct from last year
        nth_working_day_of_month_date = get_nth_working_day_of_month(nth_day, start=date(year - 1, 10, 1))
        fristen.append(FristWithAttributes(nth_working_day_of_month_date, label))

        # nov from last year
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

    def _generate_lwt_frist(self, year: int, month: int, nth_day: int, label: str):
        """
        Generate a frist with a given last working day.
        The last day in the month is counted irrespective if its a working day or not.
        """
        last_day_of_month = monthrange(year, month)[1]
        last_date_of_month = date(year, month, last_day_of_month)
        first_day_of_next_month = last_date_of_month + timedelta(days=1)
        date_dummy = get_previous_working_day(first_day_of_next_month)
        # the last day of the month counts, regardless if its a wt or not
        i_relevant_days = min(last_day_of_month - date_dummy.day, 1)
        while i_relevant_days < nth_day:
            date_dummy = get_previous_working_day(date_dummy)
            i_relevant_days += 1

        return FristWithAttributes(date_dummy, label)

    def generate_all_fristen_for_given_lwt(self, year: int, nth_day: int, label: str) -> list[FristWithAttributes]:
        """
        Generate the list of fristen for a given year that are on the nth LWT (letzer Werktag, last working day)
        of each month of the calendar.
        LWT are counted back into the month starting from the last day of the month.
        The last day of the month is counted irrespective if it is a wt or not.
        """

        fristen: list[FristWithAttributes] = []

        # dez last year
        fristen.append(self._generate_lwt_frist(year - 1, 12, nth_day, label))

        # this year
        n_months = 12
        for i_month in range(1, n_months + 1):
            fristen.append(self._generate_lwt_frist(year, i_month, nth_day, label))

        # jan next year
        fristen.append(self._generate_lwt_frist(year + 1, 1, nth_day, label))

        return fristen

    def generate_all_fristen(self, year: int) -> list[FristWithAttributes]:
        """
        Generate the list of all Fristen in the calendar for a given year
        """

        days_and_labels = [
            (5, "5WT"),
            (10, "10WT"),
            (12, "12WT"),
            (14, "14WT"),
            (16, "16WT"),
            (17, "17WT"),
            (18, "18WT"),
            (20, "20WT"),
            (21, "21WT"),
            (26, "26WT"),
            (30, "30WT"),
            (42, "42WT"),
            (0, "LWT"),
            (3, "3LWT"),
        ]
        fristen = self.generate_specific_fristen(year, days_and_labels)

        fristen.sort(key=lambda fwa: fwa.date)
        return fristen

    def generate_specific_fristen(self, year: int, days_and_labels: list[tuple[int, str]]) -> list[FristWithAttributes]:
        """
        Generate the list of Fristen in the calendar for a given year for a given set of Fristen
        The specification of the Fristen is for example: days_and_labels = [(5, '5WT'), (3, 'LWT), ...]
        The only two valid format for the label string is an integer followed by one of the two endings:
        WT (Werktag) or LWT (letzter Werktag)
        """

        fristen = []
        for days, label in days_and_labels:
            if label.endswith("LWT"):
                fristen += self.generate_all_fristen_for_given_lwt(year, days, label)
            elif label.endswith("WT"):
                fristen += self.generate_all_fristen_for_given_wt(year, days, label)
            else:
                raise ValueError(f"The label '{label}' must end with either 'WT' or 'LWT'")

        fristen.sort(key=lambda fwa: fwa.date)
        return fristen

    def create_ical_event(self, frist: FristWithAttributes) -> Event:
        """
        Create an ical event for a given frist
        """
        event = Event()
        event.add("summary", frist.label)
        event.add("dtstart", frist.date)
        event.add("dtstamp", datetime.utcnow())

        return event

    def create_ical(self, attendee: str, fristen: list[FristWithAttributes]) -> Calendar:
        """
        Create an ical calendar with a given mail address and a given set of firsten
        """
        cal = Calendar()
        cal.add("attendee", attendee)
        for frist in fristen:
            cal.add_component(self.create_ical_event(frist))

        return cal

    def export_ical(self, file_path:Path, cal: Calendar):
        """
        Write .ics file from calendar
        """
        with open(file_path, "wb") as file:
            file.write(cal.to_ical())

    def generate_and_export_whole_calendar(self, file_path:Path, attendee: str, year: int):
        """
        Generates a calendar for a given year and exports it to an .ics file
        """
        self.export_ical(file_path, self.create_ical(attendee, self.generate_all_fristen(year)))
