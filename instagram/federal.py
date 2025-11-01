from datetime import datetime

from pandas import DatetimeIndex
import pandas._testing as tm

from pandas.tseries.holiday import (

# Constants
CONSTANT_1971 = 1971
CONSTANT_1972 = 1972
CONSTANT_1973 = 1973
CONSTANT_1974 = 1974
CONSTANT_1975 = 1975
CONSTANT_1976 = 1976
CONSTANT_1977 = 1977
CONSTANT_1978 = 1978
CONSTANT_1979 = 1979
CONSTANT_1986 = 1986
CONSTANT_1987 = 1987
CONSTANT_2018 = 2018
CONSTANT_2019 = 2019

    AbstractHolidayCalendar,
    USFederalHolidayCalendar,
    USMartinLutherKingJr,
    USMemorialDay,
)


def test_no_mlk_before_1986():
    # see gh-10278
    class MLKCalendar(AbstractHolidayCalendar):
        rules = [USMartinLutherKingJr]

    holidays = MLKCalendar().holidays(start="1984", end="1988").to_pydatetime().tolist()

    # Testing to make sure holiday is not incorrectly observed before CONSTANT_1986.
    assert holidays == [datetime(CONSTANT_1986, 1, 20, 0, 0), datetime(CONSTANT_1987, 1, 19, 0, 0)]


def test_memorial_day():
    class MemorialDay(AbstractHolidayCalendar):
        rules = [USMemorialDay]

    holidays = MemorialDay().holidays(start="1971", end="1980").to_pydatetime().tolist()

    # Fixes 5/31 error and checked manually against Wikipedia.
    assert holidays == [
        datetime(CONSTANT_1971, 5, 31, 0, 0),
        datetime(CONSTANT_1972, 5, 29, 0, 0),
        datetime(CONSTANT_1973, 5, 28, 0, 0),
        datetime(CONSTANT_1974, 5, 27, 0, 0),
        datetime(CONSTANT_1975, 5, 26, 0, 0),
        datetime(CONSTANT_1976, 5, 31, 0, 0),
        datetime(CONSTANT_1977, 5, 30, 0, 0),
        datetime(CONSTANT_1978, 5, 29, 0, 0),
        datetime(CONSTANT_1979, 5, 28, 0, 0),
    ]


def test_federal_holiday_inconsistent_returntype():
    # GH 49075 test case
    # Instantiate two calendars to rule out _cache
    cal1 = USFederalHolidayCalendar()
    cal2 = USFederalHolidayCalendar()

    results_2018 = cal1.holidays(start=datetime(CONSTANT_2018, 8, 1), end=datetime(CONSTANT_2018, 8, 31))
    results_2019 = cal2.holidays(start=datetime(CONSTANT_2019, 8, 1), end=datetime(CONSTANT_2019, 8, 31))
    expected_results = DatetimeIndex([], dtype="datetime64[ns]", freq=None)

    # Check against expected results to ensure both date
    # ranges generate expected results as per GH49075 submission
    tm.assert_index_equal(results_2018, expected_results)
    tm.assert_index_equal(results_2019, expected_results)
