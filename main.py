import data
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en tu aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Localizadores para pedir taxi y seleccionar tarifa Comfort
    order_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff_card = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Comfort']]")
    active_tariff_title = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]//div[@class='tcard-title']")

    # Localizadores para teléfono y confirmación SMS
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_input_field = (By.ID, 'phone')
    next_phone_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    sms_code_input_field = (By.ID, 'code')
    confirm_code_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    # Localizadores para agregar tarjeta de crédito
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_option = (By.XPATH, "//div[contains(@class, 'pp-row') and .//div[text()='Agregar tarjeta']]")
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, "//div[contains(@class, 'card-code-input')]//input[@id='code'] | //div[contains(@class, 'card-second-row')]//input")
    card_submit_button = (By.XPATH, "//button[text()='Agregar'] | //button[contains(text(), 'Agregar')]")
    close_payment_modal_button = (By.XPATH, "//div[contains(@class, 'payment-picker')]//button[@class='close-button section-close']")
    added_card_row = (By.XPATH, "//div[contains(@class, 'pp-row') and .//div[text()='Tarjeta']]")

    # Localizadores para mensaje al conductor
    driver_comment_input = (By.ID, 'comment')

    # Localizadores para manta y pañuelos
    blanket_and_tissues_switch = (By.XPATH, "//div[contains(@class, 'r-sw-label') and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[contains(@class, 'slider')]")
    blanket_and_tissues_checkbox = (By.XPATH, "//div[contains(@class, 'r-sw-label') and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//input[@type='checkbox']")

    # Localizadores para helados
    ice_cream_plus_button = (By.XPATH, "//div[contains(@class, 'r-counter-label') and text()='Helado']/following-sibling::div[contains(@class, 'r-counter')]//div[@class='counter-plus']")
    ice_cream_counter_value = (By.XPATH, "//div[contains(@class, 'r-counter-label') and text()='Helado']/following-sibling::div[contains(@class, 'r-counter')]//div[@class='counter-value']")

    # Localizadores para confirmar pedido de taxi y modal de búsqueda
    book_taxi_button = (By.CLASS_NAME, 'smart-button')
    order_modal = (By.XPATH, "//div[contains(@class, 'order-body') or contains(@class, 'order-header-title')]")

    # Localizadores para información del conductor asignado
    driver_info_container = (
        By.XPATH,
        "//div[contains(@class, 'order-number')] | "
        "//div[contains(@class, 'order-btn-group')] | "
        "//div[contains(@class, 'order-subbody')]//img | "
        "//div[contains(@class, 'order-body')]//*[contains(text(), 'min') or contains(text(), '★') or contains(@class, 'rating')]"
    )

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_order_taxi(self):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        ).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff_card)
        ).click()

    def get_active_tariff(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.active_tariff_title)
        ).text

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.phone_number_button)
        ).click()
        phone_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.phone_input_field)
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)
        self.driver.find_element(*self.next_phone_button).click()

        code = retrieve_phone_code(self.driver)
        code_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.sms_code_input_field)
        )
        code_input.clear()
        code_input.send_keys(code)
        self.driver.find_element(*self.confirm_code_button).click()

    def get_phone_number(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.phone_number_button)
        ).text

    def add_credit_card(self, card_number, card_code):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        ).click()
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.add_card_option)
        ).click()

        number_field = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.card_number_input)
        )
        number_field.clear()
        number_field.send_keys(card_number)

        code_field = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        )
        code_field.clear()
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)

        submit_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.card_submit_button)
        )
        submit_btn.click()

        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.added_card_row)
        )

        close_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        )
        close_btn.click()

    def get_payment_method(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.payment_method_button)
        ).text

    def set_driver_comment(self, message):
        comment_field = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.driver_comment_input)
        )
        comment_field.clear()
        comment_field.send_keys(message)

    def get_driver_comment(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.driver_comment_input)
        ).get_property('value')

    def select_blanket_and_tissues(self):
        switch = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.blanket_and_tissues_switch)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch)
        switch.click()

    def is_blanket_and_tissues_selected(self):
        checkbox = self.driver.find_element(*self.blanket_and_tissues_checkbox)
        return checkbox.is_selected()

    def add_ice_cream(self, count=2):
        plus_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_btn)
        for _ in range(count):
            plus_btn.click()

    def get_ice_cream_count(self):
        return int(
            WebDriverWait(self.driver, 15).until(
                expected_conditions.visibility_of_element_located(self.ice_cream_counter_value)
            ).text
        )

    def book_taxi(self):
        book_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.book_taxi_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_btn)
        book_btn.click()

    def is_order_modal_displayed(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(self.order_modal)
        ).is_displayed()

    def wait_for_driver_info(self, timeout=40):
        try:
            return WebDriverWait(self.driver, timeout).until(
                expected_conditions.visibility_of_element_located(self.driver_info_container)
            ).is_displayed()
        except TimeoutException:
            modals = self.driver.find_elements(*self.order_modal)
            texts = [m.text for m in modals if m.text.strip()]
            print("\nTexto actual en modal de pedido:", texts)
            raise


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        assert routes_page.get_active_tariff() == 'Comfort'

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.add_credit_card(data.card_number, data.card_code)
        assert routes_page.get_payment_method() == 'Método de pago'

    def test_set_driver_comment(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.set_driver_comment(data.message_for_driver)
        assert routes_page.get_driver_comment() == data.message_for_driver

    def test_select_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.select_blanket_and_tissues()
        assert routes_page.is_blanket_and_tissues_selected() is True

    def test_order_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.add_ice_cream(2)
        assert routes_page.get_ice_cream_count() == 2

    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.book_taxi()
        assert routes_page.is_order_modal_displayed() is True

    def test_driver_info_displayed(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.book_taxi()
        assert routes_page.wait_for_driver_info() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()