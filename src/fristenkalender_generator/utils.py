"""
utility functions
"""

from datetime import datetime, timedelta
from itertools import groupby
from typing import Literal, Mapping, Optional, TypedDict

from bdew_datetimes import create_bdew_calendar

from fristenkalender_generator.bdew_calendar_generator import FristWithAttributes

_DeutscherWochentag = Literal["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

weekday_mapping: Mapping[str, _DeutscherWochentag] = {  # Mapping of %A weekdays to custom abbreviations
    "Monday": "Mo",
    "Tuesday": "Di",
    "Wednesday": "Mi",
    "Thursday": "Do",
    "Friday": "Fr",
    "Saturday": "Sa",
    "Sunday": "So",
}


class _CalendarEntry(TypedDict):
    """
    a format which is processable by Annika M. for the PDF-Fristenkalender
    """

    wochentag: _DeutscherWochentag
    datum: str  #: German format: "dd.mm.yyyy"
    fristen: Optional[list[str]]  #: e.g. ["42WT", "LWT"]
    feiertags_name: Optional[str]  # e.g. "Ostermontag"


def convert_fristen_list_to_calendar_like_dictionary(fristen: list[FristWithAttributes]) -> dict[str, _CalendarEntry]:
    """
    Sorts the list of Fristen by date such that they can be read like a calendar.
    """
    _bdew_holidays = create_bdew_calendar()  # this behaves like a dict
    result: dict[str, _CalendarEntry] = {}
    for frist_date, matching_fristen in groupby(sorted(fristen, key=lambda fwa: fwa.date), key=lambda fwa: fwa.date):
        result[frist_date.isoformat()] = _CalendarEntry(
            wochentag=weekday_mapping[frist_date.strftime("%A")],
            datum=frist_date.isoformat(),
            fristen=[fwa.label for fwa in matching_fristen],
            feiertags_name=_bdew_holidays.get(frist_date.isoformat(), None),
        )
    current_date = min(f.date for f in fristen)
    max_date = max(f.date for f in fristen)
    while current_date <= max_date:
        german_str = current_date.isoformat()
        if german_str not in result:
            result[german_str] = _CalendarEntry(
                wochentag=weekday_mapping[current_date.strftime("%A")],
                datum=german_str,
                fristen=None,
                feiertags_name=_bdew_holidays.get(current_date.isoformat(), None),
            )
        current_date += timedelta(days=1)
    result = dict(sorted(result.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d")))  # re-sort
    return result
