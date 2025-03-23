from argparse import ArgumentParser
from typing import Dict, List
from datetime import datetime, timedelta
import pandas
import platform
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ONE_DAY = timedelta(days=1)


def parse_options():
    parser = ArgumentParser()

    parser.add_argument(
        "--name", dest="name", help="Hotel name", required=False)
    parser.add_argument(
        "--start-date", dest="start", help="start date", required=False)
    parser.add_argument(
        "--end-date", dest="end", help="end date", required=False)
    parser.add_argument(
        "--from-csv-file", dest="from_csv_file",
        help="Provide names and check in/out dates from a csv file",
        required=False, default=None
    )
    return parser.parse_args()


def get_screenshot(driver: Chrome, file_name: str) -> None:
    """
    get screenshot
    """
    with open(file_name, "wb") as png:
        png.write(driver.get_screenshot_as_png())


def wait_for_element_to_stale(
        driver: Chrome, elem: WebElement, timeout: int = 10):
    '''
    wait for the given elem to be stale
    '''
    WebDriverWait(driver, timeout).until(
        EC.staleness_of(elem)
    )


def get_driver():
    """
    """
    if platform.system() != "Darwin":
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式 (Headless Mode)
        chrome_options.add_argument("--no-sandbox")  # 避免權限問題
        chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享內存不足問題
        chrome_options.add_argument("--disable-gpu")  # 在無頭模式下需要禁用 GPU
        chrome_options.add_argument("--disable-setuid-sandbox")  # 在容器內運行時必須禁用
        chrome_options.add_argument("--window-size=1920,1080")
        return Chrome(options=chrome_options)
    else:
        return Chrome()


def get_price_from_row(row: WebElement) -> str:
    """
    get the hotel prices from a row
    """
    class_names = ('nDkDDb', 'iqYCVb', 'MW1oTb', 'UeIHqb')

    for class_name in class_names:
        try:
            if row.find_element(By.CLASS_NAME, class_name).text:
                return row.find_element(By.CLASS_NAME, class_name).text
        except NoSuchElementException:
            pass

    return ''


def open_all_options(driver: Chrome) -> None:
    """
    一直按查看更多選項，直到沒有為止
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[jsname="wQivvd"]'))
        ).click()
    except TimeoutException:
        print("沒有更多選項")
        return
    except StaleElementReferenceException:
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[jsname="wQivvd"]'))
            ).click()
        except StaleElementReferenceException:
            pass

    while True:
        try:
            driver.find_element(By.CLASS_NAME, "bbRZy").click()
        except ElementNotInteractableException:
            return
        except NoSuchElementException:
            return


def set_checkin_date(driver: Chrome, date: str):
    """
    set checkin date
    """
    checkin = driver.find_element(
        By.CSS_SELECTOR, '[placeholder="登機報到頁面"]')
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[jsname="Z186"]'))
        )
    except TimeoutException:
        elem = None
    checkin.send_keys(
        Keys.BACK_SPACE * len(checkin.get_attribute("value")) +
        date + Keys.ENTER)

    if elem:
        try:
            wait_for_element_to_stale(driver, elem)
        except TimeoutException:
            print("Element not stale after setting checkin date.")


def set_checkout_date(driver: Chrome, date: str):
    """
    set checkin date
    """
    checkin = driver.find_element(By.CSS_SELECTOR, '[placeholder="退房"]')
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[jsname="Z186"]'))
        )
    except TimeoutException:
        elem = None
    checkin.send_keys(
        Keys.BACK_SPACE * len(checkin.get_attribute("value")) +
        date + Keys.ENTER)
    if elem:
        try:
            wait_for_element_to_stale(driver, elem, 10)
        except TimeoutException:
            print("Element not stale after setting checkout date")


def get_hotel_prices(
        name: str, checkin_date: str, checkout_date: str) -> List[Dict]:
    """
    get the hotel price by given name and check in/out date
    """
    driver = get_driver()
    driver.get(f"https://www.google.com/travel/search?q={name}&hl=zh-Hant-CA")

    set_checkin_date(driver, checkin_date)
    set_checkout_date(driver, checkout_date)

    # 查看更多選項
    open_all_options(driver)

    file_name: str = f"{name}_{checkin_date}_{checkout_date}.png"
    with open(file_name, "wb") as png:
        png.write(driver.get_screenshot_as_png())
    try:
        all_options = [
            elem for elem in driver.find_elements(
                By.CSS_SELECTOR, '[jsname="Z186"]')
            if elem.text != ''][-1]
    except IndexError:
        print(f"找不到{name}在{checkin_date}和{checkout_date}之間的價錢")
        return []

    prices = []
    for row in all_options.find_elements(By.CSS_SELECTOR, '.ADs2Tc'):
        try:
            ota = row.find_element(
                By.CSS_SELECTOR, '[data-click-type="268"]').text
            price = get_price_from_row(row)
            if price:
                prices.append({"OTA": ota, "price": price})
        except NoSuchElementException:
            print(row.text)
        except StaleElementReferenceException:
            print("Row stale")
    driver.quit()
    return prices


def dump_day_by_day_price_to_excel(name: str, start_date: str, end_date: str):
    """
    """
    start = datetime.strptime(start_date, "%m月%d日")
    end = datetime.strptime(end_date, "%m月%d日") + ONE_DAY
    data = {}
    while start < end:
        checkin = datetime.strftime(start, "%m月%d日")
        checkout = datetime.strftime(start + ONE_DAY, "%m月%d日")
        key = "_".join((checkin, checkout))
        data[key] = get_hotel_prices(name, checkin, checkout)
        start += ONE_DAY
    with pandas.ExcelWriter(f"{name}.xlsx", engine="xlsxwriter") as writer:
        for sheet_name, records in data.items():
            df = pandas.DataFrame(records)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    options = parse_options()
    if options.from_csv_file is None:
        dump_day_by_day_price_to_excel(
            options.name, options.start, options.end)
    else:
        reader = pandas.read_csv(options.from_csv_file)
        for row in reader.to_dict(orient="records"):
            dump_day_by_day_price_to_excel(
                row['name'], row['start'], row['end'])


if __name__ == "__main__":
    main()
