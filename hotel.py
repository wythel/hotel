from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver: Chrome = Chrome()
driver.get("https://www.google.com/travel/search?q=台北福華大飯店&hl=zh-Hant-CA")

all_options = driver.find_element(By.CSS_SELECTOR, '[jsname="Z186"]')
# elements = driver.find_elements(By.CLASS_NAME, 'iqYCVb')
# print([elem.text for elem in elements])
# import pdb; pdb.set_trace()
# driver.quit()

