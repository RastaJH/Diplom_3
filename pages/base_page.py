from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.education-services.ru"
        self.wait = WebDriverWait(driver, 10)
    
    def open(self, path=""):
        self.driver.get(self.base_url + path)
    
    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def find_clickable_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def click(self, locator, timeout=10):
        element = self.find_clickable_element(locator, timeout)
        element.click()
    
    def get_text(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        return element.text
    
    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_invisible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def is_element_displayed(self, locator, timeout=5):
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def wait_for_text_to_be_present(self, locator, text, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def scroll_to_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element
    
    def wait_for_page_loaded(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )