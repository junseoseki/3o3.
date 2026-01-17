from src.page.loginpage import loginpage
from src.util.locator import mainpage_locator as M
from playwright.sync_api import expect

def test_login(page):
    # conftest.py의 auth_state 덕분에 이미 로그인된 상태로 시작합니다.
    page.goto("/") # base_url로 이동
    
    page.wait_for_timeout(3000) # 렌더링 대기
    expect(page.locator(M.refund_hospital_bills_BTN)).to_contain_text("병원비 환급액 확인하기", timeout=10000)
    
