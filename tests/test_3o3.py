from src.page.loginpage import loginpage
from playwright.sync_api import expect
from src.util.locator import login_locator as L
from src.util.locator import mainpage_locator as M

def test_login_scenario(page):
    login = loginpage(page)
    login.try_login()
    expect(page.locator(L.id_input)).to_be_visible()
    expect(page.locator(L.password_input)).to_be_visible()
    expect(page.locator(L.login_button)).to_be_visible()
    expect(page.locator(L.qr_login_button)).to_be_visible()
    
def test_login_negative(page):
    login = loginpage(page)
    login.try_login_with_testid()
    login._wait_for_load_state()
    expect(page.locator(M.check_already_form)).to_be_visible()
