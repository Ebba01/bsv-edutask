import pytest
import json
import os


class FileHandler:
    def __init__(self, filename):
        with open(filename, 'r') as readfile:
            self.file = json.load(readfile)

    def getContent(self):
        return self.file


class TestFileHandler:

    @pytest.fixture
    def filehandler(self):
        filepath = "temp_test_file.json"

        # 🔹 Setup: skapa fil
        data = {"name": "Jane", "age": 25}
        with open(filepath, "w") as f:
            json.dump(data, f)

        handler = FileHandler(filepath)

        # 🔹 yield = ge till testet
        yield handler

        # 🔹 Teardown: ta bort fil
        if os.path.exists(filepath):
            os.remove(filepath)

    @pytest.mark.unit
    def test_getContent(self, filehandler):
        result = filehandler.getContent()

        assert result == {"name": "Jane", "age": 25}