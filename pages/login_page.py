from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.path = "/login"
    
    def login(self, email, password):
        self.open(self.path)
        self.find_clickable_element(self.EMAIL_INPUT).send_keys(email)
        self.find_clickable_element(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)