import pytest
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "base_url": os.getenv("MAIN_URL"),
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ko-KR",
        "timezone_id": "Asia/Seoul"
    }

@pytest.fixture(autouse=True)
def auto_visit_base_url(page):
    page.goto("/")
    yield
    page.close()    

# 실패 시 스크린샷을 Allure 리포트에 첨부하는 Hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # page fixture가 있는지 확인
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            import allure
            # 스크린샷 첨부
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
    