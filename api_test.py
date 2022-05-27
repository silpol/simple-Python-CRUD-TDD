import requests
import pytest, pexpect

class TestAPI():
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = 'http://localhost:80'

    @pytest.fixture(autouse=True)
    def start_server(self):
        server = pexpect.spawn("docker compose up --build pythonapp")
        server.expect('Running on http://127.0.0.1:80')
        yield
        server.kill(9)

    def test_API_OK(self):
        r = requests.get("http://localhost:80/api")
        assert r.status_code == 200
        assert r.json() == {"API":"OK"}

'''
test plans

1) per each type of object
-- double insert to check 500 on constraints
-- double delete to check 500 on constraints
-- update with empty string in name to check constraints
-- inserts and updates with too long name

-- Continent should have delete propagation
-- Country should have delete propagation
'''
