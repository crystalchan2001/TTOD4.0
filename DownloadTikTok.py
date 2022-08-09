import VideoMethods as VM
import pandas as pd
import cv2

url1 = "https://www.tiktok.com/@bmwusa?lang=en"
url2 = "https://www.tiktok.com/@therock?lang=en"
url3 = "https://www.tiktok.com/@olympics?lang=en"

#* Uses csv from ScrapeTikTok.py to pandas Data Frame
#* Sorts and filters the csv and downloads the videos from url into frames
    
# Sorts the given dataframe (default by Views) and returns top x (def 10) videos
def sortBy(df, col='Views', topx=10):
    sortedDF = df.sort_values(by=[col], ascending=False)
    return sortedDF.head(topx)

def saveSorted(df, pathIn):
    urls = df["Video URL"].tolist()
    for url in urls:
        VM.saveFrames(url, pathIn, 50)

def test():
    nfl_df = pd.read_csv('nfl.csv')
    print(nfl_df)
    # olympicsDF = pd.read_csv('olympics.csv')
    # olSort = sortBy(olympicsDF, 'Views', 5)
    nfl_sorted = sortBy(nfl_df, 'Likes', 5)
    print(nfl_sorted)
    saveSorted(nfl_sorted, 'sample_media/nfl_frames')

test()



