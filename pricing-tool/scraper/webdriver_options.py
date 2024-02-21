from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def firefox_options():
    options = Options()
    ff_profile = FirefoxProfile()
    options.add_argument("-headless")
    ff_profile.set_preference('permissions.default.image', 2)
    ff_profile.set_preference("javascript.enabled", False)
    options.profile = ff_profile

    return options