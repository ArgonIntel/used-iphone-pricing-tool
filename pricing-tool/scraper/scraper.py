from time import sleep
from random import randint

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from webdriver_options import firefox_options








def get_data_from_url(web_address: str) -> list[dict]:
    """Main function that handles all scraping using helper functions

    Args:
        web_address (str): URL of starting page for scraping

    Returns:
        list[dict]: Returns a list of ads data stored in a dictionary
    """
    driver = initialize_webdriver()
    driver.get(web_address)
    page = get_content_block(driver)
    links = get_ads_urls(page)
    next_page = get_next_page_url(page)
    data_list = []
    while True:
        data_list.extend(get_ads_data(driver, links))
        if next_page is None:
            break
        driver.get(next_page)
        page = get_content_block(driver)
        links = get_ads_urls(page)
        next_page = get_next_page_url(page)
    driver.quit()
    return data_list


def initialize_webdriver():
    return webdriver.Firefox(
        options=firefox_options(), service=Service(GeckoDriverManager().install())
    )


def get_content_block(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "content-main"))
    )


def get_ads_urls(page_content) -> list[str]:
    """Function returns list of URL's of individual ads

    Args:
        page_content (_type_): page that contains URL's of individual ads

    Returns:
        list[str]: List of ad URL's
    """
    ads_block = page_content.find_element(
        By.CLASS_NAME,
        "EntityList.EntityList--Standard.EntityList--Regular.EntityList--ListItemRegularAd",
    )
    links = ads_block.find_elements(By.CLASS_NAME, "entity-title")
    return [
        link.find_element(By.CLASS_NAME, "link").get_attribute("href") for link in links
    ]


def get_next_page_url(page_content) -> str:
    """Function that gets URL of next page.

    Args:
        page_content (_type_): 

    Returns:
        str: URL of the next page (pagination)
    """
    try:
        next_page_container = page_content.find_element(
            By.CLASS_NAME, "Pagination-item.Pagination-item--next"
        )
        return next_page_container.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        return None


def get_ads_data(driver, content_links: list[str]) -> list[dict]:
    """Function that iterates through the list of URL's and scrapes ads data

    Args:
        driver (webdriver): Firefox webdriver
        content_links (list[str]): list of URL's of individual ads

    Returns:
        list[dict]: List of dictionaries, each dictionary contains ad information
    """
    ads = []
    for link in content_links:
        # sleep(randint(1,3))
        driver.get(link)

        content = get_content_block(driver)
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
        driver.back()
    return ads
