import cv2
# For displaying an error in saveFrames() method 
import os, errno


# Output: (width, height)
def getSize(capIn):
    return (int(capIn.get(3)), int(capIn.get(4)))

def printSize(size):
    print("[VIDEO INFO] Width: {}, Height {}".format(size[0], size[1]))

# Output: (fps, frame_count)
def getFrames(capIn):
    return (capIn.get(5), capIn.get(7))

def printFrames(frames):
    print("[VIDEO INFO] Fps:", frames[0], "Frame count:", frames[1])

def end(capIn):
    capIn.release() #when all done, release vid capture object
    cv2.destroyAllWindows() #closes all the frames 

def printInfo(capIn):
    size = getSize(capIn)
    frames = getFrames(capIn)

    printFrames(frames)
    printSize(size)
    return [frames, size]

def playVid(vidIn, small=1):
    print("[INFO] playing video")
    # Open the video
    cap = cv2.VideoCapture(vidIn)

    size = tuple(int(ti/small) for ti in getSize(cap))

    frames = getFrames(cap)
    printFrames(frames)

    if(not cap.isOpened()): #check if video opened successfully
        print("Error opening video file")

    while(cap.isOpened()): #read until vid is complete
        ret, frame = cap.read() #capture frame by frame
        if ret:
            cv2.imshow('Frame', cv2.resize(frame, size))

            key = cv2.waitKey(30)
            if key == ord('q'): #press 'q' to exit 
                break
            if key == ord('p'): #press 'p' to pause
                cv2.waitKey(-1) #wait until any key is pressed (waits infinitely for key event)

        else:
            print("No frames")
            break

    end(cap)
    print("[INFO] video played successfully")


# Save video from link as an MP4 into the specified path input
def saveVidMP4(videoIn, pathIn):
    print("[INFO] saving video as MP4")
    cap = cv2.VideoCapture(videoIn)
    info = printInfo(cap)
    out = cv2.VideoWriter(pathIn, -1, info[0][0], info[1])

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)

            key = cv2.waitKey(10)
            if key == ord('q'): #press 'q' to exit 
                break
            if key == ord('p'): #press 'p' to pause
                cv2.waitKey(-1) #wait until any key is pressed (waits infinitely for key event)
            
        else:
            print("[INFO] video saved as MP4")
            break
    
    end(cap)
    out.release()

# Tutorial: https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/
# Saves video from link or file into path "folder/frame[x]" for every {skip} frames
def saveFrames(video, folder, skip=30):

    print("Opening", video, "and saving to path", folder)
    # vcap = cv2.VideoCapture("http://thinkingform.com/wp-content/uploads/2017/09/video-sample-mp4.mp4?_=1")
    vcap = cv2.VideoCapture(video)
    frames = getFrames(vcap)
    printFrames(frames)

    if(not vcap.isOpened()):
        print("[INFO] error reading video file")

    frame_num = 0 # Keeping track of the frame number
    while(vcap.isOpened()):
        ret, frame = vcap.read()
        if not ret: break
        if ret and frame_num % skip == 0:
            cv2.imshow('Frame', frame)        
            if cv2.waitKey(8) == ord('s'):
                break
            path = f"{folder}"
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                cv2.imwrite(f"{path}/frame{frame_num+1}.jpg", frame)
                print(frame_num)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        frame_num += 1

    end(vcap)
    print("[INFO] video was saved as", int(frame_num/skip), "frames")