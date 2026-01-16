from src.page.loginpage import loginpage
from src.util.locator import mainpage_locator as M
from playwright.sync_api import expect

def test_login(page):
    login = loginpage(page)
    login.try_login()
    expect(page.locator(M.refund_hospital_bills_BTN)).to_contain_text("병원비 환급액 확인하기")
    
