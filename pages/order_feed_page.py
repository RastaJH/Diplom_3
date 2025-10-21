from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
from .base_page import BasePage


class OrderFeedPage(BasePage):
    ORDER_FEED_SECTION = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    ORDERS_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]//li[contains(@class, 'text_type_digits-default')]")
    
    def __init__(self, driver):
        super().__init__(driver, "https://stellarburgers.education-services.ru")
    
    @allure.step("Проверить отображение раздела 'Лента заказов'")
    def is_order_feed_displayed(self):
        return self.is_element_displayed(self.ORDER_FEED_SECTION)
    
    @allure.step("Получить количество заказов за все время")
    def get_total_orders_count(self):
        try:
            count_text = self.get_text(self.TOTAL_ORDERS_COUNT)
            return int(count_text) if count_text else 0
        except (TimeoutException, ValueError):
            return 0
    
    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        try:
            count_text = self.get_text(self.TODAY_ORDERS_COUNT)
            return int(count_text) if count_text else 0
        except (TimeoutException, ValueError):
            return 0
    
    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self):
        try:
            elements = self.driver.find_elements(*self.ORDERS_IN_PROGRESS)
            return [element.text for element in elements if element.text]
        except Exception:
            return []
    
    @allure.step("Дождаться изменения счетчиков заказов")
    def wait_for_order_count_change(self, initial_total, initial_today, timeout=10):
        def counts_changed(driver):
            current_total = self.get_total_orders_count()
            current_today = self.get_today_orders_count()
            return current_total != initial_total or current_today != initial_today
        
        return self.wait_for_condition(counts_changed, timeout=timeout)