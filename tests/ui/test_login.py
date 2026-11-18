from playwright.sync_api import Page, expect

def test_login_with_valid_user_shows_accounts_overview(page: Page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

def test_login_with_wrong_password_shows_error(page:Page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("pass")
    page.get_by_role("button", name="Log In").click()
    expect(page.locator("#rightPanel")).to_contain_text("The username and password could not be verified.")

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

    # compare
    for account_id in api_ids:
        assert account_id in ui_ids
