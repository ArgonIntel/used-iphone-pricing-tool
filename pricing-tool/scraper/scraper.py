import logging

from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


class Scraper():
    def __init__(self, headless=True, image_load=False, javascript=False):
        
        #self.root_link = root_link
        #self.data_list = []
        self._options = self._firefox_options(headless, image_load, javascript)
        self._driver = self._initialize_webdriver()




    def get_data(self, root_link: str) -> list[dict]:
        """Main function that handles all scraping using helper functions

        Args:
            root_link (str): URL of starting page for scraping

        Returns:
            list[dict]: Returns a list of ads data stored in a dictionary
        """
        self._driver.get(root_link)
        _root_content = self._get_content_block()
        _links = self._get_links_list(_root_content)
        _next_page = self._get_next_page_link(_root_content)
        data_list = []
        while True:
            data_list.extend(self._get_ads_data(_links))
            if _next_page is None:
                break

            self._driver.get(_next_page)
            _root_content = self._get_content_block()
            self._links = self._get_links_list(_root_content)
            self._next_page = self._get_next_page_link(_root_content)
        self._driver.quit()
        return self.data_list

    def _firefox_options(self, headless: bool, image_load: bool, javascript: bool) -> Options:
        options = Options()
        ff_profile = FirefoxProfile()
        if headless:
            options.add_argument("-headless")
        if image_load:
            ff_profile.set_preference('permissions.default.image', 1)
        else:
            ff_profile.set_preference('permissions.default.image', 2)
        if javascript:
            ff_profile.set_preference("javascript.enabled", True)
        else:
            ff_profile.set_preference("javascript.enabled", False)
        options.profile = ff_profile

        return options

    def _initialize_webdriver(self) -> webdriver.Firefox:
        """Initializes the webdriver with the options set in the constructor

        Returns:
            webdriver.Firefox: Returns a Firefox webdriver instance
        """
        return webdriver.Firefox(
            options=self._options, service=Service(GeckoDriverManager().install())
        )

    def _get_content_block(self) -> webdriver.remote.webelement.WebElement:
        return WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content-main"))
        )

    def _get_next_page_link(self, _root_content) -> str:
        """Function that gets URL of next page.

        Args:
            _root_content (_type_): 

        Returns:
            str: URL of the next page (pagination)
        """
        try:
            next_page_container = _root_content.find_element(
                By.CLASS_NAME, "Pagination-item.Pagination-item--next"
            )
            return next_page_container.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            return None

    def _get_links_list(self, _root_content) -> list[str]:
        """Function returns list of URL's of individual ads

        Args:
            _root_content (_type_): page that contains URL's of individual ads

        Returns:
            list[str]: List of ad URL's 
        """
        ads_block = _root_content.find_element(
            By.CLASS_NAME,
            "EntityList.EntityList--Standard.EntityList--Regular.EntityList--ListItemRegularAd",
        )
        links = ads_block.find_elements(By.CLASS_NAME, "entity-title")
        return [
            link.find_element(By.CLASS_NAME, "link").get_attribute("href") for link in links
        ]



    def _get_ads_data(self, _links: list[str]) -> list[dict]:
        """Function that iterates through the list of URL's and scrapes ads data

        Args:
            _links (list[str]): list of URL's of individual ads

        Returns:
            list[dict]: List of dictionaries, each dictionary contains ad information
        """
        ads = []
        for link in _links:
            # sleep(randint(1,3))
            self._driver.get(link)

            content = self._get_content_block()
            try:
                advertiser = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailOwnerDetails-title"
                ).text
                store_private = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailOwnerDetails-linkAllAds"
                ).text.split()
                ad_title = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailSummary-title"
                ).text
                loc_state = content.find_elements(
                    By.CLASS_NAME, 'ClassifiedDetailBasicDetails-listDefinition'
                )
                location = loc_state[0].text.split(",")
                condition = loc_state[1].text
                price = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailSummary-priceDomestic"
                ).text.split()
                ad_description = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailDescription-text"
                ).text
                ad_id = content.find_element(
                    By.CLASS_NAME, "ClassifiedDetailSummary-adCode"
                ).text.split()
                dopublishing_noshowings = content.find_elements(
                    By.CLASS_NAME, "ClassifiedDetailSystemDetails-listData"
                )
                date_of_publishing = dopublishing_noshowings[0].text.split()
                number_of_showings = dopublishing_noshowings[2].text.split()
                ads.append(
                    {
                        "advertiser": advertiser,
                        "store_private": store_private[-1],
                        "ad_title": ad_title,
                        "location": location[0],
                        "condition": condition,
                        "price": price[0],
                        "ad_description": ad_description,
                        "ad_id": ad_id[-1],
                        "date_of_publishing": date_of_publishing[0],
                        "number_of_showings": number_of_showings[0],
                    }
                )
                
            except Exception as e:
                print(e)
            
            # sleep(randint(1,5))
            self._driver.back()
        return ads

        