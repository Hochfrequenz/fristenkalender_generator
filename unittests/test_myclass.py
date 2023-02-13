from datetime import date

import pytest

from fristenkalender_generator.mymodule import FristenkalenderGenerator, FristWithAttributes


class TestFristenkalenderGenerator:
    """
    A class with pytest unit tests.
    """

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
        assert (
            FristenkalenderGenerator().generate_fristen_list_variable_wt(year, nth_day, label)[0].date_of_the_frist
            == expected
        )

    def test_if_first_LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_lwt(2023)[0].date_of_the_frist == date(2022, 12, 30)

    def test_if_first_3LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_3lwt(2023)[0].date_of_the_frist == date(2022, 12, 28)

    def test_if_last_3LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_3lwt(2023)[-1].date_of_the_frist == date(2024, 1, 26)

    def test_if_last_frist_in_fristen_calender_is_right(self):
        assert FristenkalenderGenerator().generate_all_fristen_list(2023)[-1].date_of_the_frist

    @pytest.mark.parametrize(
        "year, expected",
        [
            pytest.param(2023, FristWithAttributes(date(2023, 3, 1), "42WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 3, 9), "26WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 5, 22), "14WT")),
            pytest.param(2023, FristWithAttributes(date(2023, 9, 27), "3LWT")),
        ],
    )
    def test_if_frist_is_in_fristen_calender(self, year: int, expected: FristWithAttributes):
        fristen = FristenkalenderGenerator().generate_all_fristen_list(year)
        test_frist = expected
        assert test_frist in fristen
