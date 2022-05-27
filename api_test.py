import requests
import pytest
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get("my_api_service").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    print(api_url)
    return request_session, api_url


def test_api_ok():
    r = requests.get("http://localhost:80/api")
    assert r.status_code == 200
    assert r.json() == {"API": "OK"}


'''
test plans
1) standard check of CRUD functioning
2) per each type of object / access point 
-- double insert to check 500 on constraints
-- double delete to check 500 on constraints
-- update with empty string in "name" key of JSON to check constraints
-- inserts and updates with too long "name" field
-- duplicate "correct" key name in JSON parameters,
--- one case with original "new" names (not present in db before)
--- one case with one already present and another not present
-- same plus in combination with incorrect ones (few cases possible)
3) relationships
-- _Continent_ delete should have delete cascaded to _countries_ and then to _cities_, no dormant "leaves" left
-- _Country_ should have delete propagation to _cities_, update up to _continents_, no dormant "leaves" left
'''
