import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        # CI 환경이거나 Docker 컨테이너 내부인 경우 헤드리스 모드 및 내장 Chromium 사용
        is_ci = os.getenv("CI") == "true"
        is_docker = os.path.exists("/.dockerenv")
        
        if is_ci or is_docker:
            browser = p.chromium.launch(headless=True)
        else:
            browser = p.chromium.launch(headless=False, channel="chrome")
        context = browser.new_context()
        page = context.new_page()
        page.goto(os.getenv("MAIN_URL"))
        yield page
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 스크린샷 자동 캡처 Hook
    """
    outcome = yield
    rep = outcome.get_result()
    
    # fixture에서 'page' 객체를 사용하는 테스트가 실패했을 때
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            import allure
            try:
                # 스크린샷 찍어서 Allure에 첨부
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"failed_screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"스크린샷 저장 실패: {e}")
   
