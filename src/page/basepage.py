from playwright.sync_api import Page, Locator

class basepage:
    def __init__(self, page: Page, timeout: 5000):
        self.page = page
        self.timeout = timeout

    def _get_locator(self, locator: str) -> Locator:
        return self.page.locator(locator)
    
    def _wait_for_load_state(self):
        self.page.wait_for_load_state("networkidle")