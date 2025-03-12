from argparse import ArgumentParser
import time
import json
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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
    # driver.find_element(By.CSS_SELECTOR, '[aria-label="價格"]').click()
    # time.sleep(10)
    checkin = driver.find_element(By.CSS_SELECTOR, '[placeholder="登機報到頁面"]')
    checkin.send_keys(
        Keys.BACK_SPACE * len(checkin.get_attribute("value")) +
        options.check_in + Keys.ENTER)
    time.sleep(5)
    checkout = driver.find_element(By.CSS_SELECTOR, '[placeholder="退房"]')
    checkout.send_keys(
        Keys.BACK_SPACE * len(checkout.get_attribute("value")) +
        options.check_out + Keys.ENTER)
    time.sleep(5)
    # 查看更多選項
    driver.find_element(By.CSS_SELECTOR, '[jsname="wQivvd"]').click()
    time.sleep(5)

    all_options = driver.find_elements(By.CSS_SELECTOR, '[jsname="Z186"]')[-1]
    prices = {}
    for row in all_options.find_elements(By.CSS_SELECTOR, '.ADs2Tc'):
        try:
            ota = row.find_element(By.CSS_SELECTOR, '[data-click-type="268"]').text
            price = row.find_element(By.CLASS_NAME, 'iqYCVb').text
            prices[ota] = price
        except NoSuchElementException:
            print(row.text)
    print(prices)


if __name__ == "__main__":
    main()
