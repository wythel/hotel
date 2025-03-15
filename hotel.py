from argparse import ArgumentParser
import time
from typing import Dict, List
import pandas
import platform
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def parse_options():
    parser = ArgumentParser()

    parser.add_argument(
        "--name", dest="name", help="Hotel name", required=False)
    parser.add_argument(
        "--check-in", dest="check_in", help="Check in date", required=False)
    parser.add_argument(
        "--check-out", dest="check_out", help="Checkout date", required=False)
    parser.add_argument(
        "--from-csv-file", dest="from_csv_file",
        help="Provide names and check in/out dates from a csv file",
        required=False, default=None
    )
    return parser.parse_args()


def get_hotel_prices(name: str, checkin_date: str, checkout_date: str) -> List[Dict]:
    """
    get the hotel price by given name and check in/out date
    """

    if platform.system() != "Darwin":
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式 (Headless Mode)
        chrome_options.add_argument("--no-sandbox")  # 避免權限問題
        chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享內存不足問題
        chrome_options.add_argument("--disable-gpu")  # 在無頭模式下需要禁用 GPU
        chrome_options.add_argument("--disable-setuid-sandbox")  # 在容器內運行時必須禁用
        chrome_options.add_argument("--window-size=1920,1080")
        driver = Chrome(options=chrome_options)
    else:
        driver = Chrome()

    driver.get(f"https://www.google.com/travel/search?q={name}&hl=zh-Hant-CA")

    print("Setting check-in date")
    checkin = driver.find_element(By.CSS_SELECTOR, '[placeholder="登機報到頁面"]')
    checkin.send_keys(
        Keys.BACK_SPACE * len(checkin.get_attribute("value")) +
        checkin_date + Keys.ENTER)
    time.sleep(5)
    print("Setting check-out date")
    checkout = driver.find_element(By.CSS_SELECTOR, '[placeholder="退房"]')
    checkout.send_keys(
        Keys.BACK_SPACE * len(checkout.get_attribute("value")) +
        checkout_date + Keys.ENTER)
    time.sleep(5)
    # 查看更多選項
    driver.find_element(By.CSS_SELECTOR, '[jsname="wQivvd"]').click()
    time.sleep(5)

    file_name: str = f"{name}_{checkin_date}_{checkout_date}_prices.png"
    with open(file_name, "wb") as png:
        png.write(driver.get_screenshot_as_png())

    all_options = driver.find_elements(By.CSS_SELECTOR, '[jsname="Z186"]')[-1]
    prices = []
    for row in all_options.find_elements(By.CSS_SELECTOR, '.ADs2Tc'):
        try:
            ota = row.find_element(By.CSS_SELECTOR, '[data-click-type="268"]').text
            price = row.find_element(By.CLASS_NAME, 'iqYCVb').text
            prices.append({"OTA": ota, "price": price})
        except NoSuchElementException:
            print(row.text)
    driver.quit()
    return prices


def main():
    options = parse_options()
    if options.from_csv_file is None:
        key = "_".join((options.name, options.check_in, options.check_out))
        data = {key: get_hotel_prices(
            options.name, options.check_in, options.check_out)}
    else:
        data = {}
        reader = pandas.read_csv(options.from_csv_file)
        for row in reader.to_dict(orient="records"):
            key = "_".join((row['name'], row['checkin'], row['checkout']))
            data[key] = get_hotel_prices(
                row['name'], row['checkin'], row['checkout'])

    with pandas.ExcelWriter("data.xlsx", engine="xlsxwriter") as writer:
        for sheet_name, records in data.items():
            df = pandas.DataFrame(records)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    main()
