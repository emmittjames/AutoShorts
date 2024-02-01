from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import time, re

# Config
screenshotDir = "Screenshots"
screenWidth = 768
screenHeight = 2000

def getPostScreenshots(filePrefix, script, postId, read_comments):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    print("Driver setup complete")
    driver.switch_to.window(driver.window_handles[0])
    close_popup(driver, wait)
    if read_comments:
        script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=postId)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        for commentFrame in script.frames:
            commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    else:
        script.titleSCFile = __takeStoryScreenshotsTitle(filePrefix, driver, wait, postId=postId)
        try:
            driver.find_element(By.ID, f"t3_{postId}-read-more-button").click()
        except:
            print("Read more button not found")
        for commentFrame in script.frames:
            paragraphNum = int(re.search(r'\d+$', commentFrame.commentId).group()) # get last number in the paragraph string
            commentFrame.screenShotFile = __takeStoryScreenshots(filePrefix, driver, wait, postId=postId, paragraphNum=paragraphNum)
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post", postId=""):
    if(handle == "Post"):
        close_popup(driver, wait)
        driver.switch_to.default_content()

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
    post_body = driver.find_element(By.ID, f"t3_{postId}-post-rtjson-content")
    paragraphs = post_body.find_elements(By.TAG_NAME, 'p')
    search = paragraphs[paragraphNum]
    fileName = f"{screenshotDir}/{filePrefix}-p{paragraphNum}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def combine_images_vertically(image_path1, image_path2, output_path):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    if img1.width != img2.width:
        raise ValueError("Images must have the same width")
    combined_image = Image.new('RGBA', (img1.width, img1.height + img2.height), (255, 255, 255, 0))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (0, img1.height))
    combined_image.save(output_path)

def close_popup(driver, wait):
    max_tries = 5
    for tries in range(max_tries):
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.default_content()
        all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in all_iframes:
            try:
                driver.switch_to.frame(iframe)
                # popup_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Close']")))
                popup_close_button = driver.find_element(By.CSS_SELECTOR, f"[aria-label='Close']")
                popup_close_button.click()
                print("Closed iframe")
                driver.switch_to.default_content()
                return
            except Exception as e:
                print(f"Error in iframe {iframe}")
                driver.switch_to.default_content()
        print("No Google popup found | tries:", tries)
        if tries == max_tries - 1:
            # time.sleep(5)
            raise NoSuchElementException("Couldn't close popup")

def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)

    driver.get(url)

    return driver, wait