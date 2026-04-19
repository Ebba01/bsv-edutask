import pytest
from unittest.mock import MagicMock
from src.util.helpers import ValidationHelper


@pytest.mark.unit
@pytest.mark.parametrize(
    "age, expected",
    [
        (-1, "invalid"),
        (0, "underaged"),
        (1, "underaged"),
        (17, "underaged"),
        (18, "valid"),
        (19, "valid"),
        (50, "valid"),
        (120, "valid"),
        (121, "invalid"),
    ]
)
def test_validateAge(age, expected):
    mock_usercontroller = MagicMock()
    mock_usercontroller.get.return_value = {"age": age}

    helper = ValidationHelper(mock_usercontroller)

    result = helper.validateAge("user-1")

    assert result == expected