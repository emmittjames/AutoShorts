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

# driver.set_window_size(width=screenWidth, height=screenHeight)
driver.set_window_size(770,1000)

driver.get("https://www.reddit.com/r/AskReddit/comments/18o0rhl/what_warning_signs_are_you_seeing_that_no_one_is/?rdt=64880")

try:
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    driver.find_element(By.CSS_SELECTOR, f"[aria-label='Close']").click()
    driver.switch_to.default_content()
except:
    print("No iframe found")

# thing_id = "t1_kefak5i"
thing_id = "t1_kefljv4"
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