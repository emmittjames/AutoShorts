"""
import screenshot, configparser, reddit

fileName = "testFileName"

config = configparser.ConfigParser()
config.read('config.ini')
outputDir = config["General"]["OutputDirectory"]
script, postId = reddit.getContent(outputDir, 1)

screenshot.getPostScreenshots(fileName, script, postId)
"""

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
driver.set_window_size(20,800)

driver.get("https://www.reddit.com/r/AskReddit/comments/18o0rhl/what_warning_signs_are_you_seeing_that_no_one_is/?rdt=64880")

# faceplate_batch = driver.find_element_by_css_selector("faceplate-batch")

# faceplate_batch = main_content.find_element(By.TAG_NAME, "faceplate-batch")

comment_tree = wait.until(EC.presence_of_element_located((By.ID, "comment-tree")))

shadow_root_script = '''
    return arguments[0].shadowRoot;
'''
shadow_root = driver.execute_script(shadow_root_script, comment_tree)
# comment = shadow_root.find_element(By.CSS_SELECTOR, "shreddit-comment")

# comments = wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-comment")))

# comments = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "shreddit-comment")))

"""
thingid_value = "t1_kf5jwx8"
thingid_value = "your_thingid_value"
comment_selector = f"thingid='{thingid_value}'"
comment = shadow_root.find_element(By.CSS_SELECTOR, comment_selector)
"""


# comment = shadow_root.find_element(By.CSS_SELECTOR, f"shreddit-comment[thingid='{thingid_value}']")

"""
collapse_buttons = driver.find_elements(By.ID, "comment-fold-button")

for button in collapse_buttons:
    print("click")
    button.click()
"""

# thing_id = "t1_kef1n05"
thing_id = "t1_kefak5i"
comment = driver.find_element(By.CSS_SELECTOR, f"[thingid='{thing_id}']")

shadow_root_script = "return arguments[0].shadowRoot;"
comment_shadow_root = driver.execute_script(shadow_root_script, comment)

aria_label = "Toggle Comment Thread"
comment_shadow_root.find_element(By.CSS_SELECTOR, f"[aria-label='{aria_label}']").click()

# comments = shadow_root.find_elements(By.CSS_SELECTOR, "shreddit-comment")

"""
print("lenth:", len(comments))

for comment in comments:
    driver.execute_script("window.focus();")
    random_num = random.randint(0, 100000)
    print(random_num)
    fileName = f"Screenshots/{random_num}.png"
    fp = open(fileName, "wb")
    fp.write(comment.screenshot_as_png)
    fp.close()
"""

driver.execute_script("window.focus();")
random_num = random.randint(0, 100000)
print(random_num)
fileName = f"Screenshots/{random_num}.png"
fp = open(fileName, "wb")
fp.write(comment.screenshot_as_png)
fp.close()
