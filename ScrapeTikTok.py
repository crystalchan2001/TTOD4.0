from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
# For account name extraction
import re

# Account urls used to test functions
url1 = "https://www.tiktok.com/@bmwusa?lang=en"
url2 = "https://www.tiktok.com/@therock?lang=en"
url3 = "https://www.tiktok.com/@olympics?lang=en"
# url4 = "https://www.tiktok.com/@therock/video/7121751192199384366"
# url5 = "https://www.tiktok.com/@therock/video/7120608832237325614"
url6 = "https://www.tiktok.com/@nfl?lang=en"

#* Scrapes TikTok accounts for video urls, captions and stats.
#* Saves the info into a csv anf returns a Pnadas DataFrame for each account 
#* ATM, only downloads vids viewed on the first page loaded

def createDriver(urlIn):
    print("[INFO] creating driver with url:", urlIn)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome("chromedriver.exe", options=options)
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


# Input: Link for a TikTok accont
# Calls getVidUrlAndViews 
# For each of the video links, finds the downloadble source, video captions, likes, comments and shares
# srcs[string], captions[string], views[float], likes[float], comments[float], shares[float]
# Output: Pandas DataFrame 
def getVidInfo(urlIn):
    urlsAndViews = getVidUrlAndViews(urlIn) # returns 2D list [urls, views]
    srcs = []
    captions = []
    likes = []
    comments = []
    shares = []
    start = 0
    end = 0

    # get info for x video urls
    for url in urlsAndViews[0]:      
        print("[INFO] iterating getVidInfo on", url)
        start = time.time()
        driver = createDriver(url)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        try:
            srcs.append(soup.find(class_="xgplayer-container").find('video').get('src')) # appending link as str
        except AttributeError:
            srcs.append("None")

        try:
            captions.append(soup.find(class_="tiktok-j6dmhd-ImgPoster e1yey0rl1").get('alt')) # appending caption as str
        except AttributeError:
            captions.append("None")
        
        likesCommentsShares = soup.findAll(class_="tiktok-wxn977-StrongText edu4zum2") 
        try:
            likes.append(likesCommentsShares[0].text) # append likes as str
            comments.append(likesCommentsShares[1].text) # append comments as str
            shares.append(likesCommentsShares[2].text) # append shares as str
        except IndexError:
            likes.append(None)
            comments.append(None)
            shares.append(None)
            print('[INFO] likes, comments and shares inaccessible')

        cleanUp(driver, soup)

        end = time.time()
        print("[INFO] iteration took", end-start)
        time.sleep(1)
    videos = pd.DataFrame({'Video URL':srcs, 'Caption':captions, 'Views':urlsAndViews[1], 'Likes':toInt(likes), 
                            'Comments':toInt(comments), 'Shares':toInt(shares)})

    accountName = getAccountName(urlIn)
    videos.to_csv(f'{accountName}.csv', index=False)
    return videos


def test():
    print(getVidInfo(url6))
    # print(getVidUrlAndViews(url6))

def createDF(account):
    df = getVidInfo(account)
    print(df)

    
test()    




