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
   
