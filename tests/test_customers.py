import pytest

def test_customer_has_expected_name(api, base_url):
    response = api.get(f"{base_url}/customers/12212")
    assert response.status_code == 200
    body = response.json()
    assert body["firstName"] == "John"

def test_all_accounts_belong_to_customer(api,base_url):
    response = api.get(f"{base_url}/customers/12212/accounts")
    assert response.status_code == 200
    accounts = response.json()
    for account in accounts:
        assert account["customerId"] == 12212
    
def test_unknown_customer_returns_400(api, base_url):
    response = api.get(f"{base_url}/customers/9999999")
    assert response.status_code == 400
    assert "Could not find customer" in response.text

@pytest.mark.parametrize("id, response_code", [
    pytest.param("0", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    pytest.param("99999999", 404, marks=pytest.mark.xfail(raises=AssertionError, reason="Parabank returns 400")),
    ("-1", 400),
    ("abc", 404)
])
def test_not_existing_and_invalid_customer_id(api, base_url, id, response_code):
    response = api.get(f"{base_url}/customers/{id}")
    assert response.status_code == response_code
    