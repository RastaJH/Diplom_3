from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
from .base_page import BasePage


class MainPage(BasePage):
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']")
    INGREDIENT_BUN = (By.XPATH, "(//h2[text()='Булки']/following-sibling::ul//a)[1]")
    INGREDIENT_SAUCE = (By.XPATH, "(//h2[text()='Соусы']/following-sibling::ul//a)[1]")
    INGREDIENT_FILLING = (By.XPATH, "(//h2[text()='Начинки']/following-sibling::ul//a)[1]")
    
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    INGREDIENT_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//button")
    INGREDIENT_DETAILS_NAME = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//h2")
    
    BUN_COUNTER = (By.XPATH, "(//h2[text()='Булки']/following-sibling::ul//a)[1]//p[contains(@class, 'counter')]")
    SAUCE_COUNTER = (By.XPATH, "(//h2[text()='Соусы']/following-sibling::ul//a)[1]//p[contains(@class, 'counter')]")
    FILLING_COUNTER = (By.XPATH, "(//h2[text()='Начинки']/following-sibling::ul//a)[1]//p[contains(@class, 'counter')]")
    
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    
    def __init__(self, driver):
        super().__init__(driver, "https://stellarburgers.education-services.ru")
    
    @allure.step("Нажать на 'Конструктор'")
    def click_constructor(self):
        self.wait_for_element_to_be_clickable(self.CONSTRUCTOR_BUTTON)
        self.click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_loaded()
        return self
    
    @allure.step("Нажать на 'Лента Заказов'")
    def click_order_feed(self):
        self.wait_for_element_invisible(self.INGREDIENT_MODAL)
        self.wait_for_element_to_be_clickable(self.ORDER_FEED_BUTTON)
        self.click(self.ORDER_FEED_BUTTON)
        self.wait_for_page_loaded()
        return self
    
    @allure.step("Нажать на ингредиент типа: {ingredient_type}")
    def click_ingredient(self, ingredient_type):
        if ingredient_type == "bun":
            self.wait_for_element_visible(self.BUN_SECTION)
            self.click(self.INGREDIENT_BUN)
        elif ingredient_type == "sauce":
            self.click(self.INGREDIENT_SAUCE)
        elif ingredient_type == "filling":
            self.click(self.INGREDIENT_FILLING)
        
        self.wait_for_element_visible(self.INGREDIENT_MODAL)
        return self
    
    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        self.wait_for_element_visible(self.INGREDIENT_MODAL_CLOSE)
        self.click(self.INGREDIENT_MODAL_CLOSE)
        self.wait_for_element_invisible(self.INGREDIENT_MODAL)
        return self
    
    @allure.step("Получить название ингредиента из модального окна")
    def get_ingredient_name_from_modal(self):
        self.wait_for_element_visible(self.INGREDIENT_DETAILS_NAME)
        return self.get_text(self.INGREDIENT_DETAILS_NAME)
    
    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        return self.is_element_displayed(self.INGREDIENT_MODAL)
    
    @allure.step("Получить счетчик ингредиента: {ingredient_type}")
    def get_ingredient_counter(self, ingredient_type):
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
    
    @allure.step("Перетащить ингредиент в конструктор: {ingredient_type}")
    def drag_ingredient_to_constructor(self, ingredient_type):
        if ingredient_type == "bun":
            source_locator = self.INGREDIENT_BUN
        elif ingredient_type == "sauce":
            source_locator = self.INGREDIENT_SAUCE
        elif ingredient_type == "filling":
            source_locator = self.INGREDIENT_FILLING
        
        initial_count = self.get_ingredient_counter(ingredient_type)
        
        self.drag_and_drop(source_locator, self.CONSTRUCTOR_DROP_AREA)
        
        def counter_changed(driver):
            return self.get_ingredient_counter(ingredient_type) != initial_count
        
        self.wait_for_condition(counter_changed, timeout=5, message="Счетчик ингредиента не изменился")
        return self
    
    @allure.step("Нажать кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        self.wait_for_element_to_be_clickable(self.LOGIN_BUTTON)
        self.click(self.LOGIN_BUTTON)
        return self