import cv2

# Reading image
# https://prateekvjoshi.com/2016/03/01/how-to-read-an-image-from-a-url-in-opencv-python/

# Reading and displaying the image
def readAndShow(nameIn, imageIn, desired_height=None, desired_width=None):
    image = cv2.imread(imageIn)
    h, w = image.shape[:2]
    if desired_height!= None:
        ratio = desired_height/h
        h = desired_height
        w = int(w * ratio)
    if desired_width != None:
        ratio = desired_width/w
        w = desired_width 
        h = int(h * ratio)
    resize = cv2.resize(image, (w, h))
    print("Height = {}, Width = {}".format(h, w))
    cv2.imshow(nameIn, resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Testing the function
readAndShow("Woman violating Goldfish", 'sample_media/goldie.jpg')
readAndShow("Woman violating Goldfish Resized", 'sample_media/goldie.jpg', None, 1000)


#resizing while keeping the image dimension ratio
# desired_width = 1000
# ratio = desired_width / w
# dimensions = (desired_width, int(h * ratio))
# resized = cv2.resize(image, dimensions)
# cv2.imshow("Woman violating Goldfish", resized)
# cv2.waitKey(0)

#* Extracting RGB values of pixels
# (B, G, R) = image[random.randint(h), random.randint(w)]

# print("R = {}, G = {}, B = {}".format(R, G, B))

# B = image[100, 100, 0]
# print("B = {}".format(B))

# #Download from online
# online_img = cv2.imread('https://raw2.github.com/scikit-image/scikit-image.github.com/master/_static/img/logo.png')
# cv2.imshow('Some Logo', online_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

