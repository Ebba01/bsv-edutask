import pytest
from bson.objectid import ObjectId
from src.util.dao import DAO


@pytest.fixture
def dao():
    dao = DAO("user")
    yield dao
    dao.drop()


def test_create_valid_user(dao):
    data = {
        "firstName": "Bob",
        "lastName": "Bengt",
        "email": "bob@test.com"
    }
    result = dao.create(data)
    assert result is not None
    assert result["firstName"] == "Bob"
    assert result["lastName"] == "Bengt"
    assert result["email"] == "bob@test.com"


def test_create_user_missing_firstname(dao):
    data = {
        "lastName": "Bengt",
        "email": "bob@test.com"
    }
    with pytest.raises(Exception):
        dao.create(data)

def test_create_user_missing_Lastname(dao):
    data = {
        "firstName": "Bob",
        "email": "bob@test.com"
    }
    with pytest.raises(Exception):
        dao.create(data)

def test_create_user_missing_email(dao):
    data = {
        "firstName": "Bob",
        "lastName": "Bengt"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_user_wrong_type_firstname(dao):
    data = {
        "firstName": 123,
        "lastName": "Bengt",
        "email": "bob@test.com"
    }
    with pytest.raises(Exception):
        dao.create(data)

def test_create_user_wrong_type_lastname(dao):
    data = {
        "firstName": "Bob",
        "lastName": 123,
        "email": "bob@test.com"
    }
    with pytest.raises(Exception):
        dao.create(data)

def test_create_user_wrong_type_email(dao):
    data = {
        "firstName": "Bob",
        "lastName": "Bengt",
        "email": 123
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_user_valid_with_tasks(dao):
    tasks = ObjectId()
    data = {
        "firstName": "Bob",
        "lastName": "Bengt",
        "email": "bob@test.com",
        "tasks": [tasks]
    }
    result = dao.create(data)
    assert result is not None
    assert result["tasks"][0]["$oid"] == str(tasks)

def test_create_user_wrong_tasks_type(dao):
    data = {
        "firstName": "Bob",
        "lastName": "Bengt",
        "email": "bob@test.com",
        "tasks": ["not_objectid"]
    }
    with pytest.raises(Exception):
        dao.create(data)