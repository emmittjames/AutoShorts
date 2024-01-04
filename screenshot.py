from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Config
screenshotDir = "Screenshots"
screenWidth = 770
screenHeight = 800

def getPostScreenshots(filePrefix, script, postId):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    print("Driver setup complete")
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=postId)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=""):
    driver.execute_script("window.focus();")
    if(handle == "Post"):
        tries = 0
        while tries < 3:
            try:
                # iframe = driver.find_element(By.TAG_NAME, "iframe")
                iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                driver.switch_to.frame(iframe)
                driver.find_element(By.CSS_SELECTOR, f"[aria-label='Close']").click()
                print("closed iframe")
                tries += 999
            except:
                print("No iframe found | tries:", tries)
                tries+=1
                driver.execute_script("window.focus();")
        driver.switch_to.default_content()

        # search = wait.until(EC.presence_of_element_located((By.ID, 't3_' + postId)))
        search = driver.find_element(By.ID, 't3_' + postId)
    else:
        search = driver.find_element(By.CSS_SELECTOR, f"[thingid='{handle}']")
        try:
            shadow_root_script = "return arguments[0].shadowRoot;"
            comment_shadow_root = driver.execute_script(shadow_root_script, search)
            comment_shadow_root.find_element(By.CSS_SELECTOR, f"[aria-label='Toggle Comment Thread']").click()
        except:
            # print("No comment collapser found")
            pass
            
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)

    driver.get(url)

    return driver, wait