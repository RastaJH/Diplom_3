from selenium.webdriver.common.by import By
import allure
from .base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    
    def __init__(self, driver):
        super().__init__(driver, "https://stellarburgers.education-services.ru")
        self.path = "/login"
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        email_field = self.find_clickable_element(self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        return self
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        password_field = self.find_clickable_element(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    @allure.step("Нажать кнопку 'Войти'")
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
        return self
    
    @allure.step("Выполнить вход с email: {email}")
    def login(self, email, password):
        self.open(self.path)
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self