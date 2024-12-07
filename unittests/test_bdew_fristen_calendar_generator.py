from datetime import date
from pathlib import Path
from typing import Optional, Union

import pytest
from icalendar import vText  # type: ignore[import]
from syrupy import snapshot

from fristenkalender_generator.bdew_calendar_generator import (
    FristenkalenderGenerator,
    FristenType,
    FristWithAttributes,
    FristWithAttributesAndType,
)


class TestFristenkalenderGenerator:
    """
    Testing the methods of FristenkalenderGenerator.
    The output is tested against the existing calendar for the year 2023.
    """

    @pytest.mark.parametrize(
        "frist, expected",
        [
            pytest.param(
                FristWithAttributes(
                    date(2023, 1, 2),
                    "42WT",
                    ref_not_in_the_same_month=10,
                    description="BK-Abrechnung (BIKO ⟶ BKV)",
                ),
                vText("42WT (⭐10)"),
            ),
            pytest.param(
                FristWithAttributesAndType(
                    date(2024, 1, 26),
                    "3LWT",
                    fristen_type=FristenType.GPKE,
                    ref_not_in_the_same_month=None,
                    description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
                ),
                vText("3LWT"),
            ),
        ],
    )
    def test_create_ical_event(self, frist: Union[FristWithAttributes, FristWithAttributesAndType], expected: vText):
        assert FristenkalenderGenerator().create_ical_event(frist)["SUMMARY"] == expected

    @pytest.mark.parametrize(
        "fristen",
        [
            pytest.param(
                [
                    FristWithAttributes(
                        date(2023, i, 1), "21WT", ref_not_in_the_same_month=None, description="NKP (VNB ⟶ MGV)"
                    )
                    for i in range(1, 6)
                ]
            ),
            pytest.param(
                [
                    FristWithAttributesAndType(
                        date(2023, i, 26),
                        "3LWT",
                        fristen_type=FristenType.GPKE,
                        ref_not_in_the_same_month=None,
                        description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
                    )
                    for i in range(1, 6)
                ]
            ),
        ],
    )
    def test_create_ical(self, fristen: list[Union[FristWithAttributes, FristWithAttributesAndType]]):
        attendee = "nicola.soeker@hochfrquenz.de"
        expected = 5
        cal = FristenkalenderGenerator().create_ical(attendee, fristen)
        assert len(cal.subcomponents) == expected

    def test_create_and_export_whole_calender(self):
        # if you don't want to see the files generated from this test uncomment following lines
        # , tmpdir_factory
        # test_dir_name = "test_dir"
        # mydir = tmpdir_factory.mktemp(test_dir_name)
        attendee = "mail@test.de"
        year = 2023
        filename = "2023.ics"
        # my_file = Path(mydir) / Path(filename)
        my_file = Path(filename)
        FristenkalenderGenerator().generate_and_export_whole_calendar(my_file, attendee, year)

        assert my_file.is_file()
        assert my_file.stat().st_size != 0

    def test_create_and_export_fristen_for_type(self):
        # if you don't want to see the files generated from this test uncomment following lines
        # , tmpdir_factory
        # test_dir_name = "test_dir"
        # mydir = tmpdir_factory.mktemp(test_dir_name)
        attendee = "mail@test.de"
        year = 2023
        fristen_type = FristenType.MABIS
        filename = "MABIS.ics"
        # my_file = Path(mydir) / Path(filename)
        my_file = Path(filename)
        FristenkalenderGenerator().generate_and_export_fristen_for_type(my_file, attendee, year, fristen_type)

        assert my_file.is_file()
        assert my_file.stat().st_size != 0

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
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 3, 1),
                    label="42WT",
                    ref_not_in_the_same_month=12,
                    description="BK-Abrechnung (BIKO ⟶ BKV)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 3, 9),
                    label="26WT",
                    ref_not_in_the_same_month=1,
                    description="NKP MG-Überlappung (VNB ⟶ MGV)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 5, 22),
                    label="14WT",
                    ref_not_in_the_same_month=None,
                    description="BK-Summen vorl./endg. BRW (MGV ⟶ BKV)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 9, 27),
                    label="3LWT",
                    ref_not_in_the_same_month=None,
                    description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2024, 1, 30), label="21WT", ref_not_in_the_same_month=None, description="NKP (VNB ⟶ MGV)"
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 4, 28),
                    label="LWT",
                    ref_not_in_the_same_month=None,
                    description="BK-Zuordnungsliste (VNB ⟶ BKV)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 7, 26),
                    label="3LWT",
                    ref_not_in_the_same_month=None,
                    description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
                ),
            ),
            pytest.param(
                2023,
                FristWithAttributes(
                    date(2023, 12, 27),
                    label="3LWT",
                    ref_not_in_the_same_month=None,
                    description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
                ),
            ),
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
                date=date(2022, 12, 28),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 1, 26),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 2, 23),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 3, 28),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 4, 26),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 5, 25),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 6, 27),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 7, 26),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 8, 28),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 9, 27),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 10, 26),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 11, 27),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2023, 12, 27),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
            FristWithAttributesAndType(
                date=date(2024, 1, 26),
                label="3LWT",
                fristen_type=FristenType.GPKE,
                ref_not_in_the_same_month=None,
                description="Letzter Termin Anmeldung asynchrone Bilanzierung (Strom)",
            ),
        ]

        assert fristen_with_attr_and_type == expected

    @pytest.mark.snapshot
    def test_full_calendar_2023(self, snapshot):
        generator = FristenkalenderGenerator()
        actual = generator.generate_all_fristen(2023)
        calendar = generator.create_ical("snapshot@hochfrequenz.de", actual)
        ics_path = Path(__file__).parent / "snapshots_ics" / "2023.ics"
        FristenkalenderGenerator().export_ical(ics_path, calendar)
        snapshot.assert_match(actual)

    @pytest.mark.snapshot
    def test_full_calendar_2024(self, snapshot):
        generator = FristenkalenderGenerator()
        actual = generator.generate_all_fristen(2024)
        calendar = generator.create_ical("snapshot@hochfrequenz.de", actual)
        ics_path = Path(__file__).parent / "snapshots_ics" / "2024.ics"
        FristenkalenderGenerator().export_ical(ics_path, calendar)
        snapshot.assert_match(actual)

    @pytest.mark.parametrize(
        "frist_date, label, expected",
        [
            pytest.param(
                date(2023, 9, 12),
                "30WT",
                (
                    "Digitaler Hochfrequenz Fristenkalender \n\n30. Werktag des Fristenmonats September 2023 \n\nletztmalig Datenannahme zur 1. BK-Abrechnung beim BIKO\n\n Um die Kalendereignisse einfach zu löschen, geben sie \n'Hochfrequenz Fristenkalender' in das Suchfeld ihrer Kalenderapp ein \nund bearbeiten sie die Liste nach Wunsch.\n\nHochfrequenz Unternehmensberatung GmbH\nNördliche Münchner Straße 27A\nD-82031 Grünwald\nhttps://www.hochfrequenz.de/"
                ),
                id="",
            )
        ],
    )
    def test_generate_frist_description(self, frist_date: date, label: str, expected: str):
        actual = FristenkalenderGenerator().generate_frist_description(frist_date, label)
        assert actual == expected

    @pytest.mark.snapshot
    def test_full_calendar_2025(self, snapshot):
        generator = FristenkalenderGenerator()
        actual = generator.generate_all_fristen(2025)
        calendar = generator.create_ical("snapshot@hochfrequenz.de", actual)
        ics_path = Path(__file__).parent / "snapshots_ics" / "2025.ics"
        FristenkalenderGenerator().export_ical(ics_path, calendar)
        # hack for pycharm: run this in the debugger and copy the value of str(actual) from the variable window
        snapshot.assert_match(actual)
