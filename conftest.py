import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages.main_page import MainPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests (chrome or firefox)")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    def fin():
        try:
            driver.quit()
        except Exception as e:
            print(f"Error during driver quit: {e}")
    
    request.addfinalizer(fin)
    return driver


@pytest.fixture
def main_page(browser):
    page = MainPage(browser)
    page.open()
    
    allure.attach(
        browser.get_screenshot_as_png(),
        name="main_page_loaded",
        attachment_type=allure.attachment_type.PNG
    )
    
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            if "browser" in item.funcargs:
                browser = item.funcargs["browser"]
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")