import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", action="append", default=[], help="browser to run tests (chrome or firefox)")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser")
        if not browsers:
            browsers = ["chrome", "firefox"]  # По умолчанию оба браузера
        metafunc.parametrize("browser", browsers, indirect=True)


@pytest.fixture
def browser(request):
    browser_name = request.param
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
    from pages.main_page import MainPage
    page = MainPage(browser)
    page.open()
    return page