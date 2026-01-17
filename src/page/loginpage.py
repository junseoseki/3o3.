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
        # Check if already logged in (Session Reuse)
        try:
            # Wait for a URL that indicates we are INSIDE the app (not on login page)
            # Based on debug logs, succesful login goes to /payment/...
            self.page.wait_for_url("**/payment/**", timeout=3000)
            logging.info("Already logged in (Session Reused). Skipping login steps.")
            return
        except:
            logging.info("Not detected as logged in. Proceeding with login flow.")
            pass # Not logged in, proceed with login flow

        self._get_locator(login_locator.kakao_login_button).click()
        self._get_locator(login_locator.id_input).fill(os.getenv("ID"))
        self._get_locator(login_locator.password_input).fill(os.getenv("PASSWORD"))
        self._get_locator(login_locator.login_button).click()
        self._wait_for_load_state()
        
        # Verify login success by checking we are not on the login page anymore
        # or waiting for a key element of the main app.
        try:
            # Wait for URL to change to the main app domain
            self.page.wait_for_url("**/app.3o3.co.kr/**", timeout=15000)
            logging.info("로그인 성공: 메인 도메인 진입 확인")
        except Exception as e:
            curr_url = self.page.url
            try:
                # Capture visible text to diagnose (e.g. Captcha, "Protective Measure", "Invalid Password")
                body_text = self.page.locator("body").inner_text()[:1000].replace('\n', ' ')
            except:
                body_text = "Could not capture body text"
            
            logging.error(f"로그인 후 리다이렉트 실패. URL: {curr_url}, Text: {body_text}")
            raise Exception(f"Login Verification Failed. URL: {curr_url}, Content: {body_text}") from e