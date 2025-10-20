from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from .base_page import BasePage


class MainPage(BasePage):
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/following-sibling::ul")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки']/following-sibling::ul")
    
    FIRST_BUN = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul//a[1]")
    FIRST_SAUCE = (By.XPATH, "//h2[text()='Соусы']/following-sibling::ul//a[1]")
    FIRST_FILLING = (By.XPATH, "//h2[text()='Начинки']/following-sibling::ul//a[1]")
    
    INGREDIENT_MODAL = (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']")
    INGREDIENT_MODAL_CLOSE = (By.CSS_SELECTOR, "[class*='Modal_modal'] [class*='Modal_close']")
    INGREDIENT_DETAILS_NAME = (By.CSS_SELECTOR, "[class*='Modal_modal'] h2")
    
    BUN_COUNTER = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul//a[1]//p[contains(@class, 'counter')]")
    SAUCE_COUNTER = (By.XPATH, "//h2[text()='Соусы']/following-sibling::ul//a[1]//p[contains(@class, 'counter')]")
    FILLING_COUNTER = (By.XPATH, "//h2[text()='Начинки']/following-sibling::ul//a[1]//p[contains(@class, 'counter')]")
    
    
    CONSTRUCTOR_DROP_AREA = (By.CSS_SELECTOR, "[class*='BurgerConstructor_basket__list']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_constructor(self):
        self.wait_for_element_to_be_clickable(self.CONSTRUCTOR_BUTTON)
        self.click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_loaded()
    
    def click_order_feed(self):
        self.wait_for_element_invisible(self.INGREDIENT_MODAL)
        self.wait_for_element_to_be_clickable(self.ORDER_FEED_BUTTON)
        self.click(self.ORDER_FEED_BUTTON)
        self.wait_for_page_loaded()
    
    def click_ingredient(self, ingredient_type="bun"):
        if ingredient_type == "bun":
            self.wait_for_element_visible(self.BUN_SECTION)
            self.wait_for_element_to_be_clickable(self.FIRST_BUN)
            self.click(self.FIRST_BUN)
        elif ingredient_type == "sauce":
            self.wait_for_element_visible(self.SAUCE_SECTION)
            self.wait_for_element_to_be_clickable(self.FIRST_SAUCE)
            self.click(self.FIRST_SAUCE)
        elif ingredient_type == "filling":
            self.wait_for_element_visible(self.FILLING_SECTION)
            self.wait_for_element_to_be_clickable(self.FIRST_FILLING)
            self.click(self.FIRST_FILLING)
        
        self.wait_for_element_visible(self.INGREDIENT_MODAL)
    
    def close_ingredient_modal(self):
        self.wait_for_element_visible(self.INGREDIENT_MODAL_CLOSE)
        self.click(self.INGREDIENT_MODAL_CLOSE)
        self.wait_for_element_invisible(self.INGREDIENT_MODAL)
    
    def get_ingredient_name_from_modal(self):
        self.wait_for_element_visible(self.INGREDIENT_DETAILS_NAME)
        return self.get_text(self.INGREDIENT_DETAILS_NAME)
    
    def is_ingredient_modal_visible(self):
        return self.is_element_displayed(self.INGREDIENT_MODAL)
    
    def get_ingredient_counter(self, ingredient_type="bun"):
        try:
            if ingredient_type == "bun":
                counter_element = self.find_element(self.BUN_COUNTER, timeout=5)
            elif ingredient_type == "sauce":
                counter_element = self.find_element(self.SAUCE_COUNTER, timeout=5)
            elif ingredient_type == "filling":
                counter_element = self.find_element(self.FILLING_COUNTER, timeout=5)
            
            counter_text = counter_element.text
            return int(counter_text) if counter_text and counter_text.isdigit() else 0
        except TimeoutException:
            return 0
    
    def drag_ingredient_to_constructor(self, ingredient_type="bun"):
        if ingredient_type == "bun":
            source = self.find_element(self.FIRST_BUN)
        elif ingredient_type == "sauce":
            source = self.find_element(self.FIRST_SAUCE)
        elif ingredient_type == "filling":
            source = self.find_element(self.FIRST_FILLING)
        
        target = self.scroll_to_element(self.CONSTRUCTOR_DROP_AREA)
        
        self.wait_for_element_visible(self.CONSTRUCTOR_DROP_AREA)
        
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target).perform()
        
        initial_count = self.get_ingredient_counter(ingredient_type)
        
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.get_ingredient_counter(ingredient_type) != initial_count
        )
    
    def wait_for_ingredient_counter_increase(self, ingredient_type="bun", initial_count=0, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.get_ingredient_counter(ingredient_type) > initial_count
            )
            return True
        except TimeoutException:
            return False
    
    def click_login_button(self):
        self.wait_for_element_to_be_clickable(self.LOGIN_BUTTON)
        self.click(self.LOGIN_BUTTON)