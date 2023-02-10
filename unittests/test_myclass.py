from datetime import date

from fristenkalender_generator.mymodule import FristenkalenderGenerator


class TestFristenkalender_generator:
    """
    A class with pytest unit tests.
    """

    def test_if_first_10WT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_variable_wt(2023, 10, "10WT")[
            0
        ].date_of_the_frist == date(2022, 12, 14)

    def test_if_first_5WT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_variable_wt(2023, 5, "5WT")[
            0
        ].date_of_the_frist == date(2022, 12, 7)

    def test_if_first_12WT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_variable_wt(2023, 12, "12WT")[
            0
        ].date_of_the_frist == date(2022, 12, 16)

    def test_if_first_14WT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_variable_wt(2023, 14, "14WT")[
            0
        ].date_of_the_frist == date(2022, 12, 20)

    def test_if_first_42WT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_variable_wt(2023, 42, "42WT")[
            0
        ].date_of_the_frist == date(2022, 12, 5)

    def test_if_first_LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_lwt(2023)[0].date_of_the_frist == date(2022, 12, 30)

    def test_if_first_3LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_3lwt(2023)[0].date_of_the_frist == date(2022, 12, 28)

    def test_if_last_3LWT_day_is_right(self):
        assert FristenkalenderGenerator().generate_fristen_list_3lwt(2023)[-1].date_of_the_frist == date(2024, 1, 26)

    def test_if_last_frist_in_fristen_calender_is_right(self):
        assert FristenkalenderGenerator().generate_all_fristen_list(2023)[-1].date_of_the_frist
