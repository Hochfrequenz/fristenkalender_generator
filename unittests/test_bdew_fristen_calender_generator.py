import datetime
from datetime import date

import pytest
from icalendar import vText

from fristenkalender_generator.bdew_calender_generator import FristenkalenderGenerator, FristWithAttributes


class TestFristenkalenderGenerator:
    """
    Testing the methods of FristenkalenderGenerator.
    The output is tested against the existing calender for the year 2023.
    """

    def test_create_ical_event(self):
        frist = FristWithAttributes(date(2023, 1, 1), "21WT")
        expected = vText("21WT")

        assert FristenkalenderGenerator().create_ical_event(frist)["SUMMARY"] == expected

    def test_create_ical(self):
        fristen = [FristWithAttributes(date(2023, i, 1), "21WT") for i in range(1, 6)]
        attendee = "nicola.soeker@hochfrquenz.de"
        expected = 5
        cal = FristenkalenderGenerator().create_ical(attendee, fristen)
        assert len(cal.subcomponents) == expected

    @pytest.mark.parametrize(
        "year, nth_day, label, expected",
        [
            pytest.param(2023, 10, "10WT", date(2022, 12, 14)),
            pytest.param(2023, 5, "5WT", date(2022, 12, 7)),
            pytest.param(2023, 12, "12WT", date(2022, 12, 16)),
            pytest.param(2023, 14, "14WT", date(2022, 12, 20)),
            pytest.param(2023, 42, "42WT", date(2022, 12, 5)),
        ],
    )
    def test_generate_friste_list_variable_wt(self, year: int, nth_day: int, label: str, expected: date):
        assert FristenkalenderGenerator().generate_all_fristen_for_given_wt(year, nth_day, label)[0].date == expected

    def test_if_duplicates_are_in_fristen_calender(self):
        fristen = FristenkalenderGenerator().generate_all_fristen(2023)

        assert len(fristen) == len(set(fristen)), "There are duplicates in the list"

    @pytest.mark.parametrize(
        "year, expected",
        [
            pytest.param(2023, FristWithAttributes(date(2023, 3, 1), "42WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 3, 9), "26WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 5, 22), "14WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 9, 27), "3LWT")),
            pytest.param(2023, FristWithAttributes(date(2024, 1, 30), "21WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 4, 28), "LWT")),
            pytest.param(2023, FristWithAttributes(date(2023, 7, 26), "3LWT")),
            pytest.param(2023, FristWithAttributes(date(2023, 12, 27), "3LWT")),
        ],
    )
    def test_if_frist_is_in_fristen_calender(self, year: int, expected: FristWithAttributes):
        fristen = FristenkalenderGenerator().generate_all_fristen(year)
        test_frist = expected
        assert test_frist in fristen

    def test_generate_specific_fristen(self):
        expected = FristenkalenderGenerator().generate_all_fristen_for_given_lwt(2023, 3, "3LWT")
        expected += FristenkalenderGenerator().generate_all_fristen_for_given_wt(2023, 5, "5WT")
        expected.sort(key=lambda fwa: fwa.date)
        days_and_labels = [(3, "3LWT"), (5, "5WT")]
        assert FristenkalenderGenerator().generate_specific_fristen(2023, days_and_labels) == expected

    def test_full_calendar_2023(self):
        """
        This reference data set was checked against the existing calender from 2032 by a human.
        """
        fristen = FristenkalenderGenerator().generate_all_fristen(2023)
        # hack for pycharm: run this in the debugger and copy the value of str(fristen) from the variable window
        expected = [
            FristWithAttributes(date=datetime.date(2022, 12, 1), label="21WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 5), label="42WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 8), label="26WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 14), label="30WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 16), label="12WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 22), label="16WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 23), label="17WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 27), label="18WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 28), label="3LWT"),
            FristWithAttributes(date=datetime.date(2022, 12, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 30), label="21WT"),
            FristWithAttributes(date=datetime.date(2022, 12, 30), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 1, 2), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 9), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 9), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 13), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 16), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 18), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 24), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 25), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 26), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 26), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 1, 30), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 31), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 31), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 1, 31), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 2, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 7), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 13), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 16), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 22), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 23), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 23), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 2, 24), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 28), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 2, 28), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 3, 1), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 1), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 9), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 15), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 15), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 17), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 21), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 23), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 24), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 27), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 28), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 3, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 30), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 31), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 3, 31), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 4, 6), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 11), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 14), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 18), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 20), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 24), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 26), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 26), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 4, 27), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 28), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 4, 28), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 5, 3), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 3), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 4), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 8), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 11), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 15), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 17), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 17), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 22), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 24), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 25), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 25), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 5, 26), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 31), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 5, 31), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 6, 1), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 6), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 9), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 15), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 15), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 19), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 21), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 23), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 26), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 27), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 27), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 6, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 30), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 6, 30), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 7, 3), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 7), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 13), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 18), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 24), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 25), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 26), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 26), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 7, 28), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 31), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 31), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 7, 31), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 8, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 7), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 11), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 17), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 21), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 23), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 24), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 25), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 28), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 8, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 30), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 30), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 8, 31), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 9, 6), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 12), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 18), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 21), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 25), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 26), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 27), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 27), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 9, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 29), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 9, 29), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 10, 2), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 9), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 10), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 16), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 16), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 18), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 24), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 25), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 26), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 26), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 10, 30), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 10, 30), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 11, 2), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 3), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 8), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 9), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 15), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 15), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 17), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 21), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 24), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 27), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 27), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 11, 28), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 30), label="20WT"),
            FristWithAttributes(date=datetime.date(2023, 11, 30), label="LWT"),
            FristWithAttributes(date=datetime.date(2023, 12, 1), label="21WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 4), label="42WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 7), label="5WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 8), label="26WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 14), label="10WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 14), label="30WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 18), label="12WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 20), label="14WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 22), label="16WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 27), label="17WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 27), label="3LWT"),
            FristWithAttributes(date=datetime.date(2023, 12, 28), label="18WT"),
            FristWithAttributes(date=datetime.date(2023, 12, 29), label="LWT"),
            FristWithAttributes(date=datetime.date(2024, 1, 2), label="20WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 3), label="21WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 4), label="42WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 8), label="5WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 10), label="26WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 15), label="10WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 16), label="30WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 17), label="12WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 19), label="14WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 23), label="16WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 24), label="17WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 25), label="18WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 26), label="3LWT"),
            FristWithAttributes(date=datetime.date(2024, 1, 29), label="20WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 30), label="21WT"),
            FristWithAttributes(date=datetime.date(2024, 1, 31), label="LWT"),
        ]
        assert fristen == expected
