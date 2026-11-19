from playwright.sync_api import Page, expect

def test_ui_shows_all_accounts_from_api(page: Page, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts")
    assert response.status_code == 200 
    api_ids = [str(account["id"]) for account in response.json()]
    assert api_ids
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()
    links = page.locator("#accountTable a")
    expect(links.first).to_be_visible()
    ui_ids = links.all_inner_texts()

    for account_id in api_ids:
        assert account_id in ui_ids

def test_greeting_message_uses_correct_customer_name(page:Page, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212")
    assert response.status_code == 200
    body = response.json()
    assert body
    customer_first_name = body["firstName"]
    customer_last_name = body["lastName"]
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.locator("#leftPanel")).to_contain_text("Welcome")
    expect(page.locator("#leftPanel")).to_contain_text(f" {customer_first_name} {customer_last_name}")

def test_account_type_is_presented_correctly_in_ui(page:Page, api, api_base_url):
    response = api.get(f"{api_base_url}/customers/12212/accounts/")
    assert response.status_code == 200
    body = response.json()
    assert body
    account_id = body[0]["id"]
    account_type = body[0]["type"]
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.locator("#leftPanel")).to_contain_text("Welcome")
    page.get_by_role("link", name=str(account_id), exact=True).click()
    expect(page.get_by_role("heading", name="Account Details")).to_be_visible()
    expect(page.locator("#accountId")).to_have_text(f"{account_id}")
    expect(page.locator("#accountType")).to_have_text(f"{account_type}")

