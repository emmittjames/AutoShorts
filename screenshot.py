from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time, re

# Config
screenshotDir = "Screenshots"
screenWidth = 770
screenHeight = 800

def getPostScreenshots(filePrefix, script, postId, read_comments):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    print("Driver setup complete")
    if read_comments:
        script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=postId)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        for commentFrame in script.frames:
            commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    else:
        script.titleSCFile = __takeStoryScreenshotsTitle(filePrefix, driver, wait, postId=postId)
        for commentFrame in script.frames:
            paragraphNum = int(re.search(r'\d+$', commentFrame.commentId).group())
            commentFrame.screenShotFile = __takeStoryScreenshots(filePrefix, driver, wait, postId=postId, paragraphNum=paragraphNum)
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=""):
    driver.switch_to.window(driver.window_handles[0])
    if(handle == "Post"):
        close_popup(driver, wait)
        # search = wait.until(EC.presence_of_element_located((By.ID, 't3_' + postId)))
        # search = driver.find_element(By.ID, 't3_' + postId)
        search = driver.find_element(By.ID, f"t3_{postId}")
    else:
        search = driver.find_element(By.CSS_SELECTOR, f"[thingid='{handle}']")
        try:
            shadow_root_script = "return arguments[0].shadowRoot;"
            comment_shadow_root = driver.execute_script(shadow_root_script, search)
            comment_shadow_root.find_element(By.CSS_SELECTOR, f"[aria-label='Toggle Comment Thread']").click()
        except:
            # print("No comment collapser found")
            pass
    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __takeStoryScreenshotsTitle(filePrefix, driver, wait, postId):
    close_popup(driver, wait)
    creditBar = driver.find_element(By.CSS_SELECTOR, f"[slot='credit-bar']")
    fileName1 = f"{screenshotDir}/{filePrefix}-creditBar.png"
    fp = open(fileName1, "wb")
    fp.write(creditBar.screenshot_as_png)
    fp.close()

    postTitle = driver.find_element(By.CSS_SELECTOR, f"[slot='title']")
    fileName2 = f"{screenshotDir}/{filePrefix}-postTitle.png"
    fp = open(fileName2, "wb")
    fp.write(postTitle.screenshot_as_png)
    fp.close()

    fileNameFinal = f"{screenshotDir}/{filePrefix}-combinedHeader.png"
    combine_images_vertically(fileName1, fileName2, fileNameFinal)
    
    return fileNameFinal

def __takeStoryScreenshots(filePrefix, driver, wait, postId, paragraphNum):
    post_body = search = driver.find_element(By.ID, f"{postId}-post-rtjson-content")
    paragraphs = post_body.find_elements(By.TAG_NAME, 'p')

    # for paragraph in paragraphs:
    search = paragraphs[paragraphNum]
    fileName = f"{screenshotDir}/{filePrefix}-p{paragraphNum}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def combine_images_vertically(image_path1, image_path2, output_path):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)
    if img1.width != img2.width:
        raise ValueError("Images must have the same width")
    combined_image = Image.new('RGB', (img1.width, img1.height + img2.height))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (0, img1.height))
    combined_image.save(output_path)

def close_popup(driver, wait):
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
            driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.default_content()

def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)

    driver.get(url)

    return driver, wait