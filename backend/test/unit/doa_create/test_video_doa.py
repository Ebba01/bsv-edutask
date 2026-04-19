import pytest
from src.util.dao import DAO


@pytest.fixture
def dao():
    dao = DAO("video")
    yield dao
    dao.drop()


def test_create_valid_video(dao):
    data = {
        "url": "https://youtube.com/watch?v=funnyCats"
    }
    result = dao.create(data)
    assert result is not None
    assert result["url"] == "https://youtube.com/watch?v=funnyCats"


def test_create_video_missing_url(dao):
    data = {}
    with pytest.raises(Exception):
        dao.create(data)


def test_create_video_wrong_type(dao):
    data = {
        "url": 123
    }
    with pytest.raises(Exception):
        dao.create(data)