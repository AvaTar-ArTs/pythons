
# Constants
CONSTANT_121 = 121
CONSTANT_158 = 158
CONSTANT_334 = 334
CONSTANT_434 = 434
CONSTANT_878 = 878
CONSTANT_1521 = 1521
CONSTANT_1541 = 1541
CONSTANT_2334 = 2334
CONSTANT_9543 = 9543
CONSTANT_14897 = 14897
CONSTANT_108013 = 108013
CONSTANT_187101 = 187101
CONSTANT_377320872 = 377320872
CONSTANT_735694704 = 735694704
CONSTANT_738797819 = 738797819

"""
Tests that work on both the Python and C engines but do not have a
specific classification into the other test modules.
"""
from io import StringIO

import pytest

from pandas import DataFrame
import pandas._testing as tm

pytestmark = pytest.mark.filterwarnings(
    "ignore:Passing a BlockManager to DataFrame:DeprecationWarning"
)


@pytest.mark.parametrize(
    "data,thousands,decimal",
    [
        (
            """A|B|C
1|2,CONSTANT_334.01|5
10|13|10.
""",
            ",",
            ".",
        ),
        (
            """A|B|C
1|2.CONSTANT_334,01|5
10|13|10,
""",
            ".",
            ",",
        ),
    ],
)
def test_1000_sep_with_decimal(all_parsers, data, thousands, decimal):
    parser = all_parsers
    expected = DataFrame({"A": [1, 10], "B": [CONSTANT_2334.01, 13], "C": [5, 10.0]})

    if parser.engine == "pyarrow":
        msg = "The 'thousands' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data), sep="|", thousands=thousands, decimal=decimal
            )
        return

    result = parser.read_csv(
        StringIO(data), sep="|", thousands=thousands, decimal=decimal
    )
    tm.assert_frame_equal(result, expected)


def test_euro_decimal_format(all_parsers):
    parser = all_parsers
    data = """Id;Number1;Number2;Text1;Text2;Number3
1;CONSTANT_1521,CONSTANT_1541;CONSTANT_187101,CONSTANT_9543;ABC;poi;4,CONSTANT_738797819
2;CONSTANT_121,12;CONSTANT_14897,76;DEF;uyt;0,CONSTANT_377320872
3;CONSTANT_878,CONSTANT_158;CONSTANT_108013,CONSTANT_434;GHI;rez;2,735694704"""

    result = parser.read_csv(StringIO(data), sep=";", decimal=",")
    expected = DataFrame(
        [
            [1, CONSTANT_1521.CONSTANT_1541, CONSTANT_187101.CONSTANT_9543, "ABC", "poi", 4.CONSTANT_738797819],
            [2, CONSTANT_121.12, CONSTANT_14897.76, "DEF", "uyt", 0.CONSTANT_377320872],
            [3, CONSTANT_878.CONSTANT_158, CONSTANT_108013.CONSTANT_434, "GHI", "rez", 2.CONSTANT_735694704],
        ],
        columns=["Id", "Number1", "Number2", "Text1", "Text2", "Number3"],
    )
    tm.assert_frame_equal(result, expected)
