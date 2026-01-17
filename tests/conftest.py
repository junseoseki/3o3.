import pytest
import os
from playwright.sync_api import Page
from playwright_stealth import Stealth
from dotenv import load_dotenv

load_dotenv()

# 1. Configure Browser Launch (Headless, Proxy, Anti-bot args)
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # Check for proxy in env
    proxy_server = os.getenv("PROXY_URL")
    
    args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--disable-gpu",
        "--disable-infobars",
        "--window-position=0,0",
        "--ignore-certificate-errors",
        "--window-size=1920,1080",
    ]
    
    launch_options = {
        **browser_type_launch_args,
        "args": args,
        "headless": True if os.getenv("CI") == "true" else False,
        # "channel": "chrome", # Removed to use bundled Chromium which is safer in CI
    }

    if proxy_server:
        print(f"Using Proxy: {proxy_server}")
        launch_options["proxy"] = {"server": proxy_server}
        
    return launch_options

# 2. Configure Context (User Agent, Locale, Storage State)
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Standard, High-Quality User Agent (Recent Chrome on Linux)
    # Matching the OS is good practice. Linux for CI.
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    context_options = {
        **browser_context_args,
        "user_agent": USER_AGENT,
        "locale": "ko-KR",
        "viewport": {"width": 1920, "height": 1080},
        "java_script_enabled": True,
        "bypass_csp": True,
    }
    
    # Session Reuse (if available)
    state_path = ".auth/state.json"
    if os.path.exists(state_path):
        print(f"LOADING STORAGE STATE FROM: {state_path}")
        context_options["storage_state"] = state_path
    
    return context_options

# 3. Apply Stealth to every page
@pytest.fixture(autouse=True)
def apply_stealth(page: Page):
    # Apply stealth scripts to the page
    Stealth().apply_stealth_sync(page)
    
    # Additional manual evasions if stealth isn't enough
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Navigate to base URL automatically? 
    # Usually better to let test do it, but previous setup did it.
    # We'll leave navigation to the test (test_3o3.py)
    # But if we need to verify login logic implicitly like before, we might.
    # Let's clean up and let the test drive navigation.
    yield page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Auto Screenshot on Failure
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            import allure
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"failed_screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                # Also attach HTML for debugging login page blocks
                allure.attach(
                    page.content(),
                    name=f"failed_page_source_{item.name}",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
   
