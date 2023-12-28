from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

options = webdriver.FirefoxOptions()
options.headless = False
options.enable_mobile = False
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)

driver.set_window_size(770,1000)

driver.get("https://www.reddit.com/r/AskReddit/comments/18s2a7w/who_is_the_scariest_nuclear_threat_today_and_why/?rdt=36768")

try:
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    driver.find_element(By.CSS_SELECTOR, f"[aria-label='Close']").click()
except:
    print("No iframe found")

driver.switch_to.default_content()

thing_id = "t1_kf4ugu5"
comment = driver.find_element(By.CSS_SELECTOR, f"[thingid='{thing_id}']")

try:
    shadow_root_script = "return arguments[0].shadowRoot;"
    comment_shadow_root = driver.execute_script(shadow_root_script, comment)
    comment_shadow_root.find_element(By.CSS_SELECTOR, f"[aria-label='Toggle Comment Thread']").click()
except:
    print("No comment collapser found")


driver.execute_script("window.focus();")
random_num = random.randint(0, 100000)
print(random_num)
fileName = f"Screenshots/{random_num}.png"
fp = open(fileName, "wb")
fp.write(comment.screenshot_as_png)
fp.close()