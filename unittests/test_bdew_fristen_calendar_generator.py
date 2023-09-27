from datetime import date
from pathlib import Path

import pytest
from icalendar import vText  # type: ignore[import]

from fristenkalender_generator.bdew_calendar_generator import (
    FristenkalenderGenerator,
    FristenType,
    FristWithAttributes,
    FristWithAttributesAndType,
)

from .full_years import all_fristen_2023, all_fristen_2024


class TestFristenkalenderGenerator:
    """
    Testing the methods of FristenkalenderGenerator.
    The output is tested against the existing calendar for the year 2023.
    """

    def test_create_ical_event(self):
        frist = FristWithAttributes(date(2023, 1, 1), "21WT", ref_not_in_the_same_month=False)
        expected = vText("21WT")

        assert FristenkalenderGenerator().create_ical_event(frist)["SUMMARY"] == expected

    def test_create_ical(self):
        fristen = [FristWithAttributes(date(2023, i, 1), "21WT", ref_not_in_the_same_month=False) for i in range(1, 6)]
        attendee = "nicola.soeker@hochfrquenz.de"
        expected = 5
        cal = FristenkalenderGenerator().create_ical(attendee, fristen)
        assert len(cal.subcomponents) == expected

    def test_create_and_export_whole_calender(self, tmpdir_factory):
        test_dir_name = "test_dir"
        mydir = tmpdir_factory.mktemp(test_dir_name)
        attendee = "mail@test.de"
        year = 2023
        filename = "example.ics"
        my_file = Path(mydir) / Path(filename)
        FristenkalenderGenerator().generate_and_export_whole_calendar(my_file, attendee, year)

        assert my_file.is_file()
        assert my_file.stat().st_size != 0

    @pytest.mark.parametrize(
        "year, nth_day, label, expected",
        [
            pytest.param(2023, 10, "10WT", date(2022, 12, 14)),
            # pytest.param(2023, 5, "5WT", date(2022, 12, 7)),
            # pytest.param(2023, 12, "12WT", date(2022, 12, 16)),
            # pytest.param(2023, 14, "14WT", date(2022, 12, 20)),
            # pytest.param(2023, 42, "42WT", date(2022, 12, 5)),
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
            pytest.param(2023, FristWithAttributes(date(2023, 3, 1), label="42WT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 3, 9), label="26WT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 5, 22), label="14WT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 9, 27), label="3LWT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2024, 1, 30), label="21WT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 4, 28), label="LWT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 7, 26), label="3LWT", ref_not_in_the_same_month=False)),
            pytest.param(2023, FristWithAttributes(date(2023, 12, 27), label="3LWT", ref_not_in_the_same_month=False)),
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

    def test_generate_fristen_for_type(self):
        fristen_with_attr_and_type = FristenkalenderGenerator().generate_fristen_for_type(2023, FristenType.GPKE)

        expected = [
            FristWithAttributesAndType(
                date=date(2022, 12, 28), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 1, 26), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 2, 23), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 3, 28), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 4, 26), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 5, 25), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 6, 27), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 7, 26), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 8, 28), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 9, 27), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 10, 26), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 11, 27), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2023, 12, 27), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
            FristWithAttributesAndType(
                date=date(2024, 1, 26), label="3LWT", fristen_type=FristenType.GPKE, ref_not_in_the_same_month=False
            ),
        ]

        assert fristen_with_attr_and_type == expected

    @pytest.mark.parametrize(
        "year,expected",
        [
            pytest.param(
                2023,
                all_fristen_2023,
                id="This reference data set was checked against the existing calendar from 2023 by a human.",
            ),
            pytest.param(
                2024,
                all_fristen_2024,
                id="not yet checked manually⚠",
            ),
        ],
    )
    def test_full_calendar_for_a_single_year(self, year: int, expected: list[FristWithAttributes]):
        actual = FristenkalenderGenerator().generate_all_fristen(year)
        # hack for pycharm: run this in the debugger and copy the value of str(actual) from the variable window
        assert actual == expected
