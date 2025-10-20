from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    ORDER_FEED_SECTION = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    ORDERS_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]//li[contains(@class, 'text_type_digits-default')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_order_feed_displayed(self):
        return self.is_element_displayed(self.ORDER_FEED_SECTION)
    
    def get_total_orders_count(self):
        try:
            count_text = self.get_text(self.TOTAL_ORDERS_COUNT)
            return int(count_text) if count_text else 0
        except (TimeoutException, ValueError):
            return 0
    
    def get_today_orders_count(self):
        try:
            count_text = self.get_text(self.TODAY_ORDERS_COUNT)
            return int(count_text) if count_text else 0
        except (TimeoutException, ValueError):
            return 0
    
    def get_orders_in_progress(self):
        try:
            elements = self.driver.find_elements(*self.ORDERS_IN_PROGRESS)
            return [element.text for element in elements if element.text]
        except Exception:
            return []
    
    def wait_for_order_count_change(self, initial_total, initial_today, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.get_total_orders_count() != initial_total or
                    self.get_today_orders_count() != initial_today
                )
            )
            return True
        except TimeoutException:
            return False