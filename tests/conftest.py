import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from src.page.loginpage import loginpage

load_dotenv()

@pytest.fixture(scope="session")
def auth_state(tmp_path_factory):
    """
    외부에서 생성된 auth.json 파일의 경로를 반환합니다.
    이 파일은 generate_auth.py를 통해 미리 생성되어 있어야 합니다.
    """
    state_file = "auth.json"
    
    # 파일 존재 확인 (선택 사항)
    if not os.path.exists(state_file):
        # CI에서는 파일이 없을 때 경고하거나 에러를 낼 수 있음
        # 하지만 pytest-playwright는 파일이 없으면 그냥 무시하고 빈 상태로 시작할 수도 있음
        # 여기서는 명시적으로 에러를 내지 않고 경로만 반환 (없으면 로그인 안된 상태로 테스트 실패할 것임)
        print(f"경고: {state_file} 파일이 없습니다. 비로그인 상태로 테스트가 진행될 수 있습니다.")
        
    return state_file

@pytest.fixture(scope="session")
def browser_context_args(auth_state):
    """
    모든 테스트가 위에서 생성된 auth.json 상태를 로드하여 시작하도록 설정합니다.
    """
    return {
        "storage_state": auth_state,
        "base_url": os.getenv("MAIN_URL") # 이렇게 하면 test에서 page.goto("/")로 이동 가능
    }

   
