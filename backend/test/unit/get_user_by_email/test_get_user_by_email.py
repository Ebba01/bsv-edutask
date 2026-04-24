import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


class TestGetUserByEmail:

    @pytest.fixture
    def mock_dao(self):
        return MagicMock()

    @pytest.fixture
    def user_controller(self, mock_dao):
        return UserController(dao=mock_dao)

    @pytest.mark.unit
    def test_returns_user_when_exactly_one_match(self, user_controller, mock_dao):
        user = {"id": "1", "email": "anna@example.com", "name": "Anna"}
        mock_dao.find.return_value = [user]

        result = user_controller.get_user_by_email("anna@example.com")

        assert result == user

    @pytest.mark.unit
    def test_returns_first_user_when_multiple_matches(self, user_controller, mock_dao, capsys):
        user1 = {"id": "1", "email": "anna@example.com", "name": "Anna"}
        user2 = {"id": "2", "email": "anna@example.com", "name": "Annika"}
        mock_dao.find.return_value = [user1, user2]

        result = user_controller.get_user_by_email("anna@example.com")
        captured = capsys.readouterr()

        assert result == user1
        assert "more than one user found with mail anna@example.com" in captured.out

    @pytest.mark.unit
    def test_returns_none_when_no_user_matches(self, user_controller, mock_dao):
        mock_dao.find.return_value = []

        result = user_controller.get_user_by_email("missing@example.com")

        assert result is None

    @pytest.mark.unit
    def test_raises_value_error_for_invalid_email(self, user_controller, mock_dao):
        with pytest.raises(ValueError):
            user_controller.get_user_by_email("invalid-email")

        mock_dao.find.assert_not_called()

    @pytest.mark.unit
    def test_reraises_exception_when_dao_fails(self, user_controller, mock_dao):
        mock_dao.find.side_effect = Exception("database failure")

        with pytest.raises(Exception, match="database failure"):
            user_controller.get_user_by_email("anna@example.com")