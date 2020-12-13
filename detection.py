from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2


def get_point():
    image = cv2.imread('file_path')

    # im2gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    # denoise
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=1)
    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")

    # loop over the unique components
    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # set threshold
        if numPixels > 2:
            mask = cv2.add(mask, labelMask)

    # mark
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]
    points = []
    for (i, c) in enumerate(cnts):
        # mark
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        # set range
        xInArea = 1460 >= cX >= 480
        yInArea = 1160 >= cY >= 240
        print(cX, cY)
        if xInArea and yInArea:
            points.append([int(cX), int(cY)])
        # draw circles
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # show image
    image = cv2.resize(image, (683, 680))
    cv2.imshow("Image", image)
    cv2.imwrite('E:/LYK/Images/detection.jpg', image)
    cv2.waitKey(0)

    # print index
    print(points)


if __name__ == '__main__':
    get_point()
