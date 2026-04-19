import pytest
from src.util.dao import DAO


@pytest.fixture
def dao():
    dao = DAO("todo")
    yield dao
    dao.drop()


def test_create_valid(dao):
    data = {
        "description": "Pet cat",
        "done": True
    }
    result = dao.create(data)
    assert result is not None
    assert result["description"] == "Pet cat"
    assert result["done"] is True

## unik är inte unik så fel?
def test_create_unique(dao):
    data = {
        "description": "Pet cat",
        "done": True
    }
    dao.create(data)
    result = dao.create(data)
    assert result is not None
    assert result["description"] == "Pet cat"
    assert result["done"] is True

def test_create_missing_field(dao):
    data = {
        "done": True
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_wrong_type(dao):
    data = {
        "description": 123,
        "done": True
    }
    with pytest.raises(Exception):
        dao.create(data)

def test_create_done_not_bool(dao):
    data = {
        "done": 3333
    }
    with pytest.raises(Exception):
        dao.create(data)