import pytest

from fristenkalender_generator import FristenkalenderGenerator
from fristenkalender_generator.utils import _CalendarEntry, convert_fristen_list_to_calendar_like_dictionary


class TestUtils:
    @pytest.mark.parametrize(
        "expected_entries",
        [
            pytest.param(
                {
                    "01.02.2024": {
                        "datum": "01.02.2024",
                        "fristen": ["42WT"],
                        "wochentag": "Do",
                        "feiertags_name": None,
                    },
                    "01.12.2023": {
                        "datum": "01.12.2023",
                        "feiertags_name": None,
                        "fristen": ["21WT"],
                        "wochentag": "Fr",
                    },
                    "24.12.2023": {
                        "datum": "24.12.2023",
                        "feiertags_name": "Heiligabend",
                        "fristen": None,
                        "wochentag": "So",
                    },
                    "01.01.2024": {
                        "datum": "01.01.2024",
                        "feiertags_name": "Neujahr",
                        "fristen": None,
                        "wochentag": "Mo",
                    },
                },
            )
        ],
    )
    def test_conversion_to_dict(self, expected_entries: dict[str, _CalendarEntry]) -> None:
        fristen = FristenkalenderGenerator().generate_all_fristen(2024)
        actual = convert_fristen_list_to_calendar_like_dictionary(fristen)
        # I json.dumped the actual dict and sent it to Annika M. for the PDF calendar
        for key, value in expected_entries.items():
            assert actual[key] == value
