from playwright.sync_api import Page, expect
import pytest

def test_login_with_valid_user_shows_accounts_overview(page: Page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

#@pytest.mark.xfail(
        #reason="Parabank demo returns 'An internal error has occured' for a wrong password (seen Nov 19)",
        #raises = AssertionError,
#)
def test_login_with_wrong_password_shows_error(page:Page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("pass")
    page.get_by_role("button", name="Log In").click()
    expect(page.locator("#rightPanel")).to_contain_text("The username and password could not be verified.")

def test_logout_returns_to_login_page(page:Page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.locator("input[name=\"username\"]").fill("john")
    page.locator("input[name=\"password\"]").fill("demo")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()
    page.get_by_role("link", name="Log Out").click()
    expect(page.locator("#leftPanel")).to_contain_text("Customer Login")



