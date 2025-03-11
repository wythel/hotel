from argparse import ArgumentParser
import time
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def parse_options():
    parser = ArgumentParser()

    parser.add_argument(
        "--name", dest="name", help="Hotel name")
    parser.add_argument(
        "--check-in", dest="check_in", help="Check in date")
    parser.add_argument(
        "--check-out", dest="check_out", help="Checkout date")
    return parser.parse_args()


def main():
    options = parse_options()
    driver = Chrome()
    driver.get(f"https://www.google.com/travel/search?q={options.name}&hl=zh-Hant-CA")

    checkin = driver.find_element(
        By.CSS_SELECTOR, '[placeholder="登機報到頁面"]')
    checkin.send_keys(Keys.BACK_SPACE * len(checkin.get_attribute("value")) + options.check_in)
    checkout = driver.find_element(By.CSS_SELECTOR, '[placeholder="退房"]')
    checkout.send_keys(Keys.BACK_SPACE * len(checkout.get_attribute("value")) + options.check_out + Keys.ENTER)
    time.sleep(10)
    all_options = driver.find_element(By.CSS_SELECTOR, '[jsname="Z186"]')
    elements = all_options.find_elements(By.CLASS_NAME, 'iqYCVb')
    print([elem.text for elem in elements])


if __name__ == "__main__":
    main()
