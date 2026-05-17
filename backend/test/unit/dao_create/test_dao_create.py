import pytest
from unittest.mock import patch
from pymongo.errors import WriteError

from src.util.dao import DAO


TEST_COLLECTION = "test_dao_create"


@pytest.fixture
def dao():
    mock_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "description"],
            "properties": {
                "title": {
                    "bsonType": "string"
                },
                "description": {
                    "bsonType": "string"
                }
            }
        }
    }

    with patch("src.util.dao.getValidator", return_value=mock_validator):
        dao = DAO(TEST_COLLECTION)
        dao.drop()

        dao = DAO(TEST_COLLECTION)
        yield dao

        dao.drop()


def test_create_valid_object(dao):
    data = {
        "title": "Write report",
        "description": "Finish integration testing report"
    }

    result = dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["title"] == "Write report"
    assert result["description"] == "Finish integration testing report"


def test_create_missing_required_field(dao):
    data = {
        "description": "Missing title"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_wrong_data_type(dao):
    data = {
        "title": 123,
        "description": "Wrong title type"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_does_not_modify_input_data(dao):
    data = {
        "title": "Original title",
        "description": "Original description"
    }

    dao.create(data)

    assert "_id" not in data