import os
import logging
from src.page.basepage import basepage
from src.util.locator import login_locator
from dotenv import load_dotenv

load_dotenv()

class loginpage(basepage):
    def __init__(self, page, timeout=9000):
        super().__init__(page, timeout)
    
    def try_login(self):
        self._get_locator(login_locator.kakao_login_button).click()
        logging.info("로그인 페이지 진입 완료")
        
    def try_login_with_testid(self):
        self._get_locator(login_locator.id_input).fill(os.getenv("TEST_ID"))
        self._get_locator(login_locator.password_input).fill(os.getenv("TEST_PASSWORD"))
        self._get_locator(login_locator.login_button).click()
        logging.info("테스트 ID로 로그인 완료")