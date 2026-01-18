import pytest
from dotenv import load_dotenv
import os
import allure

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
    # 자동으로 메인 페이지 이동
    page.goto("/")

# 테스트가 실패했을 때, 자동으로 스크린샷을 찍어서 Allure 리포트에 붙여주는 기능(ci에서는 디버깅이 힘드니깐)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def attach_screenshot_on_failure(item, call):
    # 테스트 실행 결과를 가져옵니다.
    outcome = yield
    report = outcome.get_result()
    
    # 테스트가 실행된 시점 call이고, 결과가 실패일 때만 동작
    if report.when == "call" and report.failed:
        # 이 테스트가 page를 쓰고 있었는지 확인
        page = item.funcargs.get("page")
        
        if page:
            # 전체 화면 스크린샷을 찍어서 리포트에 첨부
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Screenshot_{item.name}", 
                attachment_type=allure.attachment_type.PNG
            )
    