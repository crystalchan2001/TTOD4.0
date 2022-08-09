from bs4 import BeautifulSoup
from selenium import webdriver
import time
import validators
import re

def createDriver(urlIn):
    print("[INFO] creating driver with url:", urlIn)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(urlIn)
    return driver

# Close and quit the driver and BeautifulSoup
def cleanUp(driverIn, soupIn):
    print("[INFO] cleaning up...")
    driverIn.quit()
    soupIn.decompose()

# Converts stats of format [string int/bs4.element][K/M/B] into a float 
def toInt(listIn):
    newItems = []
    d = { 'K' : 1, 'M' : 3, 'B' : 6}
    for item in listIn:
        itemText = item
        if type(item) not in (str, int):
            itemText = item.text
        if itemText[-1] in d:
            num, power = itemText[:-1], itemText[-1]
            newItems.append(float(num) * (1000 ** d[power]))
        else:
            newItems.append(float(itemText))
    # print("[INFO] newItems:", newItems)
    return newItems

# Uses Regex to extract the TikTok account name from the url
# If it cannot be detected, the name is default to "unnamedAccount"
def getAccountName(accountUrl):
    try:
        found = re.search('@(.+?)[?]', accountUrl)
        return found.group(1)
    except AttributeError:
        return "unnamedAccount"
        
# Input: link for a TikTok account
# Finds individual video links from the front page (num depends on time loading) and their view count
# Output: (urlList[string], viewsList[float])
def getVidUrlAndViews(accountIn):
    start = time.time()
    urlList = []
    valid = validators.url(accountIn) and accountIn.startswith("https://www.tiktok.com/@")

    if valid:
        driver = createDriver(accountIn)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        time.sleep(5)

        divWrapperList = soup.findAll(class_="tiktok-yz6ijl-DivWrapper e1cg0wnj1")
        viewsList = soup.findAll(class_="video-count tiktok-1p23b18-StrongVideoCount e148ts222")

        # print(divWrapperList[0])
        for div in divWrapperList:
            urlList.append(div.find('a').get('href'))

        cleanUp(driver, soup)
        end = time.time()

        print("[INFO] urlList length:", len(urlList))
        print("urlList:", urlList[0])
        print("[INFO] getVidUrlAndViews took", end-start, "and", end-start-5, "without sleep.")
        return (urlList, toInt(viewsList))
    else:
        return "[UNSUCCESSFUL] Please enter a valid TikTok account url in the format \"https://www.tiktok.com/@{accountName}?lang=en\""


# print(getVidUrlAndViews("https://www.tiktok.com/@bmwusa?lang=en"))

dict = {"key1":"value1"}

try:
    print(dict["key2"])
except KeyError:
    print("No key2")
    dict["key2"] = "value2"

print(dict)

try:
    print(dict["key2"])
except KeyError:
    print("No key2")
    dict["key2"] = "value2"


