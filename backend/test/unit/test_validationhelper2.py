import pytest
from unittest.mock import patch, MagicMock
from src.util.helpers import ValidationHelper2


class TestValidationHelper2:

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "age, expected",
        [
            (-1, "invalid"),
            (0, "underaged"),
            (17, "underaged"),
            (18, "valid"),   # den här kommer faila pga buggen i ValidationHelper2
            (19, "valid"),
            (120, "valid"),
            (121, "invalid"),
        ]
    )
    @patch("src.util.helpers.UserController")
    @patch("src.util.helpers.DAO")
    def test_validateAge(self, MockDAO, MockUserController, age, expected):
        mock_dao_instance = MagicMock()
        MockDAO.return_value = mock_dao_instance

        mock_usercontroller_instance = MagicMock()
        mock_usercontroller_instance.get.return_value = {"age": age}
        MockUserController.return_value = mock_usercontroller_instance

        helper = ValidationHelper2()
        result = helper.validateAge("user-1")

        assert result == expected