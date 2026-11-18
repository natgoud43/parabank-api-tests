import pytest
import requests

BASE = "https://parabank.parasoft.com/parabank/services/bank"

@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

@pytest.fixture(scope="session")
def api_base_url():
    return BASE