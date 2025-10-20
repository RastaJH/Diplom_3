import pytest
import allure
from pages.order_feed_page import OrderFeedPage
from selenium.common.exceptions import TimeoutException


@allure.feature("Основная функциональность Stellar Burgers")
class TestMainFunctionality:
    
    @allure.title("Переход по клику на 'Конструктор'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.constructor
    def test_constructor_navigation(self, main_page):
        with allure.step("Кликнуть на 'Лента заказов'"):
            main_page.click_order_feed()
        
        with allure.step("Кликнуть на 'Конструктор'"):
            main_page.click_constructor()
        
        with allure.step("Проверить, что находимся на главной странице"):
            assert main_page.find_clickable_element(main_page.LOGIN_BUTTON).is_displayed()
    
    @allure.title("Переход по клику на раздел 'Лента заказов'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.constructor
    def test_order_feed_navigation(self, main_page):
        with allure.step("Кликнуть на 'Лента заказов'"):
            main_page.click_order_feed()
        
        with allure.step("Проверить отображение раздела 'Лента заказов'"):
            order_feed_page = OrderFeedPage(main_page.driver)
            assert order_feed_page.is_order_feed_displayed()
    
    @allure.title("Открытие модального окна с деталями ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.constructor
    def test_ingredient_modal_open(self, main_page):
        with allure.step("Кликнуть на ингредиент"):
            main_page.click_ingredient("bun")
        
        with allure.step("Проверить отображение модального окна"):
            assert main_page.is_ingredient_modal_visible()
        
        with allure.step("Проверить наличие названия ингредиента"):
            ingredient_name = main_page.get_ingredient_name_from_modal()
            assert ingredient_name != ""
    
    @allure.title("Закрытие модального окна ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.constructor
    def test_ingredient_modal_close(self, main_page):
        with allure.step("Открыть модальное окно ингредиента"):
            main_page.click_ingredient("bun")
            assert main_page.is_ingredient_modal_visible()
        
        with allure.step("Закрыть модальное окно"):
            main_page.close_ingredient_modal()
        
        with allure.step("Проверить, что модальное окно закрыто"):
            assert not main_page.is_ingredient_modal_visible()
    
    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.constructor
    def test_ingredient_counter_increase(self, main_page):
        with allure.step("Получить начальное значение счетчика"):
            initial_count = main_page.get_ingredient_counter("bun")
        
        with allure.step("Добавить ингредиент в конструктор"):
            main_page.drag_ingredient_to_constructor("bun")
        
        with allure.step("Проверить увеличение счетчика"):
            new_count = main_page.get_ingredient_counter("bun")
            assert new_count > initial_count
    
    @allure.title("Добавление разных типов ингредиентов в заказ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.constructor
    def test_multiple_ingredient_counters(self, main_page):
        with allure.step("Проверить начальные счетчики"):
            bun_initial = main_page.get_ingredient_counter("bun")
            sauce_initial = main_page.get_ingredient_counter("sauce")
        
        with allure.step("Добавить булку в конструктор"):
            main_page.drag_ingredient_to_constructor("bun")
        
        with allure.step("Добавить соус в конструктор"):
            main_page.drag_ingredient_to_constructor("sauce")
        
        with allure.step("Проверить увеличение счетчиков"):
            assert main_page.get_ingredient_counter("bun") > bun_initial
            assert main_page.get_ingredient_counter("sauce") > sauce_initial
    
    @allure.title("Навигация между конструктором и лентой заказов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_navigation_between_sections(self, main_page):
        with allure.step("Проверить, что начальная страница - конструктор"):
            assert main_page.find_clickable_element(main_page.CONSTRUCTOR_BUTTON).is_displayed()
        
        with allure.step("Перейти в ленту заказов и проверить отображение"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(main_page.driver)
            assert order_feed_page.is_order_feed_displayed()
        
        with allure.step("Вернуться в конструктор и проверить отображение"):
            main_page.click_constructor()
            assert main_page.find_clickable_element(main_page.LOGIN_BUTTON).is_displayed()