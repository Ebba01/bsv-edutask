import pytest
from bson.objectid import ObjectId
from src.util.dao import DAO
from datetime import datetime, timezone


@pytest.fixture
def dao():
    dao = DAO("task")
    yield dao
    dao.drop()


def test_create_valid_task_minimal(dao):
    data = {
        "title": "Write report",
        "description": "Finish the integration testing report"
    }
    result = dao.create(data)
    assert result is not None
    assert result["title"] == "Write report"
    assert result["description"] == "Finish the integration testing report"


def test_create_valid_task_all_fields(dao):
    startdate = datetime.now(timezone.utc)
    duedate = datetime.now(timezone.utc)
    objectId = ObjectId()
    categories = ["school", "testing"]
    data = {
        "title": "Full task",
        "description": "Task with all fields",
        "startdate": startdate,
        "duedate": duedate,
        "requires": [objectId],
        "categories": categories,
        "todos": [objectId],
        "video": objectId
    }
    result = dao.create(data)
    assert result is not None
    assert result["title"] == "Full task"
    assert result["description"] == "Task with all fields"
    assert result["startdate"]["$date"] == startdate.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    assert result["duedate"]["$date"] == duedate.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    assert result["requires"][0]["$oid"] == str(objectId)
    assert result["categories"] == categories
    assert result["todos"][0]["$oid"] == str(objectId)
    assert result["video"]["$oid"] == str(objectId)


def test_create_task_missing_title(dao):
    data = {
        "description": "Missing title"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_missing_description(dao):
    data = {
        "title": "Missing description"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_title_type(dao):
    data = {
        "title": 123,
        "description": "Wrong title type"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_description_type(dao):
    data = {
        "title": "Wrong description type",
        "description": 123
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_startdate_type(dao):
    data = {
        "title": "Wrong startdate",
        "description": "Testing",
        "startdate": "2026-01-01"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_duedate_type(dao):
    data = {
        "title": "Wrong duedate",
        "description": "Testing",
        "duedate": "2026-01-01"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_requires_type(dao):
    data = {
        "title": "Wrong requires",
        "description": "Testing",
        "requires": ["not_objectid"]
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_categories_type(dao):
    data = {
        "title": "Wrong categories",
        "description": "Testing",
        "categories": [1, 2, 3]
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_todos_type(dao):
    data = {
        "title": "Wrong todos",
        "description": "Testing",
        "todos": ["not_objectid"]
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_task_wrong_video_type(dao):
    data = {
        "title": "Wrong video",
        "description": "Testing",
        "video": "not_objectid"
    }
    with pytest.raises(Exception):
        dao.create(data)