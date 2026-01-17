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
            # Add anti-detection args and Docker stability args
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu"
                ]
            )
        else:
            browser = p.chromium.launch(headless=False, channel="chrome")
        
        # Helper to load state if exists
        state_path = ".auth/state.json"
        storage_state = state_path if os.path.exists(state_path) else None
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="ko-KR",
            viewport={"width": 1920, "height": 1080},
            storage_state=storage_state
        )
        
        # Hide the webdriver property
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
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
   
