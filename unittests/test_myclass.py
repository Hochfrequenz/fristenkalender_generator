from fristenkalender_generator.mymodule import MyClass

from fristenkalender_generator.mymodule import Fristenkalender_generator

from datetime import date

class TestFristenkalender_generator:
    """
    A class with pytest unit tests.
    """

    def test_if_first_10WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 10, '10WT').loc[0,('date')] == date(2022,12,14)

    def test_if_first_5WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 5,'5WT').loc[0,('date')] == date(2022,12,7)

    def test_if_first_12WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 12,'12WT').loc[0,('date')] == date(2022,12,16)

    def test_if_first_12WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 14,'14WT').loc[0,('date')] == date(2022,12,20)

    def test_if_first_42WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 42, '42WT').loc[0, ('date')] == date(2022, 12, 5)

    def test_if_last_42WT_day_is_right(self):
        assert Fristenkalender_generator().generate_fristen_liste_variable_WT(2023, 42, '42WT').iloc[-1].date == date(2024, 1, 4)


class TestMyClass:
    """
    A class with pytest unit tests.
    """

    def test_something(self):
        my_class = MyClass()
        assert my_class.do_something() == "abc"
