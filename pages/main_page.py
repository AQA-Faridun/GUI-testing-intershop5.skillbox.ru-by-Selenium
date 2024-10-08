import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.product_card_page import ProductPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    CATALOGS: tuple[str, str] = (By.XPATH, "(//div[contains(@class,'caption wow')])")
    PRODUCTS_FROM_SALES_SECTION: tuple[str, str] = (By.CSS_SELECTOR, "aside#accesspress_store_product-2>ul>div>div>li")
    PRODUCTS_FROM_NEW_ARRIVALS_SECTION: tuple[str, str] = (By.CSS_SELECTOR, "aside#accesspress_store_product-3>ul>div>div>li")
    PRODUCT_FROM_POSTER_SECTION: tuple[str, str] = (By.ID, "accesspress_store_full_promo-2")
    PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION: tuple[str, str] = (By.XPATH, "//aside[@id='woocommerce_recently_viewed_products-2']//li")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Skillbox — Интернет магазин":
            raise Exception(f"This is not main page, current page is: {self.driver.current_url}")

    def get_catalog_and_title(self, item: int) -> tuple[WebElement, str]:
        """
        :param item: int, need point which catalog on main page you would like. Have a 3 variant
        :return: tuple[WebElement, str], catalog element and his title
        """
        with allure.step('Get catalogs'):
            catalogs: list[WebElement] = self.wait_for_elements(self.CATALOGS)

        with allure.step('Choose one of catalog'):
            catalog: WebElement = catalogs[item]

        with allure.step('Get title of choosen catalog'):
            catalog_title: str = self.get_element_from_another_element(catalog, By.TAG_NAME, "h4").text.capitalize()

        return catalog, catalog_title

    def go_to_product_from_sales_section(self, item: int) -> tuple[ProductPage, str]:
        """
        :param item: need point product on sales section in main page you would like. Have a 16 variant, but can choise only 4 cause
        of only 4 variant is visible on page
        :return: tuple[ProductPage, str], page and product title from main page
        """
        with allure.step('Get products from sales section'):
            products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_SALES_SECTION)

        with allure.step('Get one of product and scroll to it'):
            product: WebElement = products[item]
            self.scroll_to(product)

        with allure.step('Get product title'):
            header: str = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")

        with allure.step('Click on product'):
            product.click()

        return ProductPage(self.driver, header), header

    def go_to_product_from_new_arrivals_section(self, item: int) -> tuple[ProductPage, str]:
        """
        :param item: need point product on sales section in main page you would like. Have a 16 variant, but can choise only 4 cause
        of only 4 variant is visible on page
        :return: tuple[ProductPage, str], page and product title from main page
        """
        with allure.step('Get products from arrivals section'):
            products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_NEW_ARRIVALS_SECTION)

        with allure.step('Get one of the product and scroll to it'):
            product: WebElement = products[item]
            self.scroll_to(product)

        with allure.step('Get product title'):
            header: str = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")

        with allure.step('Click on product'):
            product.click()

        return ProductPage(self.driver, header), header

    def get_product_and_title_from_poster_section(self) -> tuple[ProductPage, str]:
        """
        :return:  tuple[ProductPage, str], page and product title from main page
        """
        with allure.step('Get poster and scroll to it'):
            poster: WebElement = self.wait_for_element(self.PRODUCT_FROM_POSTER_SECTION)
            self.scroll_to(poster)

        with allure.step('Get product title and button'):
            product_title: str = self.get_element_from_another_element(poster, By.CLASS_NAME, "promo-desc-title").text
            product_button: WebElement = self.wait_for_element((By.XPATH, "(//span[@class='btn promo-link-btn'])[4]"))

        with allure.step('Wait for the button to appear and click on it'):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(product_button))
            product_button.click()

        return ProductPage(self.driver, product_title), product_title

    def go_to_viewed_product(self, item: int) -> tuple[ProductPage, str]:
        """
        :param item: need point product on arrival section in main page you would like. Have a 14 variant, but can choise only 3 cause
        of only 3 variant is visible on page
        :return: tuple[ProductPage, str], page and product title from main page
        """
        header = ""
        try:
            with allure.step('Get products from viewed section'):
                products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION)

            with allure.step('Get one of the product and scroll to it'):
                product: WebElement = products[item]
                self.scroll_to(product)

            with allure.step('Get product title'):
                header: str = product.find_element(By.TAG_NAME, "span").text

            # with allure.step('Check product title for text - "Холодец-4"'):
                # if '"Холодец-4"' in header:
                #     header: str = self.replace_quotes(header)

            with allure.step('Get product link and go to it'):
                product_link: WebElement = product.find_element(By.TAG_NAME, "a")
                self.click_by(product_link)

        except TimeoutException:
            self.logger.log(30, "Cannot find viewed product block", exc_info=True)

        return ProductPage(self.driver, header), header

    # def replace_quotes(self, text: str) -> str:
    #     """Replaces double quotes with herringbones in the given text."""
    #
    #     with allure.step('Replace one type of quotes `""` to another type `«»`'):
    #         new_txt = text.replace('"', '«')
    #         last_index = new_txt.rfind('«')
    #
    #         if last_index != -1:
    #             return new_txt[:last_index] + '»' + new_txt[last_index + 1:]
    #
    #         return new_txt
