import os
import logging
from src.page.basepage import basepage
from src.util.locator import login_locator
from dotenv import load_dotenv

load_dotenv()

class loginpage(basepage):
    def __init__(self, page, timeout=5000):
        super().__init__(page, timeout)
    
    def try_login(self):
        try:
            self._get_locator(login_locator.kakao_login_button).click()
            self._get_locator(login_locator.id_input).fill(os.getenv("ID"))
            self._get_locator(login_locator.password_input).fill(os.getenv("PASSWORD"))
            self._get_locator(login_locator.login_button).click()
            logging.info("로그인 성공")
        except Exception as e:
            logging.error(f"로그인 실패: {e}")