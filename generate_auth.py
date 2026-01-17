from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from src.page.loginpage import loginpage

# 환경변수 로드 (.env 파일이 있으면 로드)
load_dotenv()

def generate_auth():
    with sync_playwright() as p:
        # 헤드리스 모드로 실행 (CI/로컬 모두 대응)
        # 디버깅을 위해 로컬에서는 headless=False로 변경해도 됨
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(os.getenv("MAIN_URL"))
        
        # 로그인 수행
        login = loginpage(page)
        login.try_login()
        
        # 로그인 완료 대기
        page.wait_for_timeout(3000)
        
        # 상태 저장
        state_file = "auth.json"
        page.context.storage_state(path=state_file)
        print(f"인증 파일 저장 완료: {state_file}")
        
        browser.close()

if __name__ == "__main__":
    try:
        generate_auth()
    except Exception as e:
        print(f"오류 발생: {e}")
        exit(1)
