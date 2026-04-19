import pytest
from unittest.mock import patch
from src.util.helpers import diceroll


@pytest.mark.unit
@pytest.mark.parametrize(
    "roll, expected",
    [
        (1, False),
        (2, False),
        (3, False),
        (4, False),  # <- denna kommer faila (bugg!)
        (5, True),
        (6, True),
    ]
)
def test_diceroll(roll, expected):
    with patch("src.util.helpers.random.randint") as mock_randint:
        mock_randint.return_value = roll

        result = diceroll()

        assert result == expected