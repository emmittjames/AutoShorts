from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(filePrefix, script, postId):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    print("Driver setup complete")
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=postId)
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=""):
    method = By.CLASS_NAME if (handle == "Post") else By.ID
    content = driver.find_element(By.ID, "main-content")
    print("take screenshot")
    if(handle == "Post"):
        print("handle = post")
        search = wait.until(EC.presence_of_element_located((By.ID, 't3_' + postId)))
    else:
        print("else")
        handle = handle + '-comment-rtjson-content'
        print("handle = " + handle)
        search = wait.until(EC.presence_of_element_located((method, handle)))
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

    # driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.set_window_size(1000,1600)

    driver.get(url)

    return driver, wait