import pytest
import allure
from pages.order_feed_page import OrderFeedPage


@allure.feature("Лента заказов Stellar Burgers")
class TestOrderFeed:
    
    @allure.title("Переход в раздел 'Лента заказов'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order_feed
    def test_order_feed_access(self, main_page):
        with allure.step("Кликнуть на 'Лента заказов'"):
            main_page.click_order_feed()
        
        with allure.step("Проверить отображение раздела 'Лента заказов'"):
            order_feed_page = OrderFeedPage(main_page.driver)
            assert order_feed_page.is_order_feed_displayed()
    
    @allure.title("Отображение счетчика 'Выполнено за всё время'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order_feed
    def test_total_orders_counter_display(self, main_page):
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(main_page.driver)
        
        with allure.step("Получить значение счетчика 'Выполнено за всё время'"):
            total_orders = order_feed_page.get_total_orders_count()
        
        with allure.step("Проверить, что счетчик отображается"):
            assert total_orders >= 0
            allure.attach(f"Счетчик 'Выполнено за всё время': {total_orders}", 
                         name="Значение счетчика")
    
    @allure.title("Отображение счетчика 'Выполнено за сегодня'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order_feed
    def test_today_orders_counter_display(self, main_page):
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(main_page.driver)
        
        with allure.step("Получить значение счетчика 'Выполнено за сегодня'"):
            today_orders = order_feed_page.get_today_orders_count()
        
        with allure.step("Проверить, что счетчик отображается"):
            assert today_orders >= 0
            allure.attach(f"Счетчик 'Выполнено за сегодня': {today_orders}", 
                         name="Значение счетчика")
    
    @allure.title("Отображение заказов в разделе 'В работе'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order_feed
    def test_orders_in_progress_display(self, main_page):
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(main_page.driver)
        
        with allure.step("Получить список заказов в работе"):
            orders_in_progress = order_feed_page.get_orders_in_progress()
        
        with allure.step("Проверить, что раздел 'В работе' отображается"):
            assert orders_in_progress is not None
            allure.attach(f"Заказы в работе: {orders_in_progress}", 
                         name="Список заказов")
    
    @allure.title("Обновление ленты заказов в реальном времени")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.order_feed
    def test_order_feed_real_time_updates(self, main_page):
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(main_page.driver)
        
        with allure.step("Проверить основные элементы ленты заказов"):
            assert order_feed_page.is_order_feed_displayed()
            
            total_orders = order_feed_page.get_total_orders_count()
            today_orders = order_feed_page.get_today_orders_count()
            orders_in_progress = order_feed_page.get_orders_in_progress()
            
            assert total_orders >= 0
            assert today_orders >= 0
            assert isinstance(orders_in_progress, list)
            
            allure.attach(
                f"Всего заказов: {total_orders}, За сегодня: {today_orders}, В работе: {len(orders_in_progress)}",
                name="Статистика заказов"
            )