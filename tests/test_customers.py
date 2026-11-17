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