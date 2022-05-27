import requests
import pytest, pexpect


class TestAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = 'http://localhost:80'

    @pytest.fixture(autouse=True)
    def start_server(self):
        server = pexpect.spawn("docker compose up --build pythonapp")
        server.expect('Running on http://127.0.0.1:80')
        yield
        server.kill(9)

    def test_api_ok(self):
        r = requests.get("http://localhost:80/api")
        assert r.status_code == 200
        assert r.json() == {"API": "OK"}


'''
test plans
1) standard check of CRUD functioning
2) per each type of object
-- double insert to check 500 on constraints
-- double delete to check 500 on constraints
-- update with empty string in name to check constraints
-- inserts and updates with too long name field
-- duplicate "correct" key name in JSON parameters,
--- one case with original "new" names (not present in db before)
--- one case with one already present and another not present
-- same plus in combination with incorrect ones (few cases possible)
3) relationships
-- Continent delete should have delete propagation to countries and then to cities, no dormant "leaves" left
-- Country should have delete propagation to cities, no dormant "leaves" left
'''
