from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import pyautogui
import time

# get the position of tip on ntmdt
print("input x position on tuscen")
x1 = int(input())
print("input y position on tuscen")
y1 = int(input())

# get the position of tip on ntmdt
print("input x posion on ntmdt")
X1 = int(input())
print("input y posion on ntmdt")
Y1 = int(input())
print(X1, Y1)

class Auto():
    def __init__(self, x1, y1, X1, Y1):
        self.x = x1
        self.y = y1
        self.x1 = X1
        self.y1 = Y1

    def get_x1(self):
        return self.x1

    def get_y1(self):
        return self.y1

    def get_X1(self):
        return self.X1

    def get_Y1(self):
        return self.Y1

    def get_mouse(self):
        time.sleep(5)
        try:
            for i in range(5):
                # Get and print the mouse coordinates.
                x, y = pyautogui.position()
                positionStr = 'position（X,Y）is：{},{}'.format(str(x).rjust(4), str(y).rjust(4))
                pix = pyautogui.screenshot().getpixel((x, y))
                positionStr += ' RGB:(' + str(pix[0]).rjust(3) + ',' + str(pix[1]).rjust(3) + ',' + str(pix[2]).rjust(
                    3) + ')'
                print(positionStr)
                time.sleep(0.5)
        except:
            print('getting position failed')

    def delete_type(self,):
        pyautogui.press('Delete')
        pyautogui.press('Delete')
        pyautogui.press('Delete')
        pyautogui.press('Delete')
        pyautogui.press('Delete')
        time.sleep(2)
        pyautogui.press('Enter')
        pyautogui.typewrite(''.format())
        time.sleep(2)

    def move(self, a, b, dur, sleep_time):
        pyautogui.moveTo(a, b, duration=dur)
        pyautogui.click()
        time.sleep(sleep_time)

    def get_point(self):
        image = cv2.imread('E:/LYK/Images/particle_1_1.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        labels = measure.label(thresh, neighbors=8, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            if numPixels > 3:
                mask = cv2.add(mask, labelMask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = contours.sort_contours(cnts)[0]
        points = []
        distances = []
        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            xInArea = cX <= 1460 and cX >= 480
            yInArea = cY <= 1160 and cY >= 240
            if xInArea and yInArea:
                points.append([int(cX), int(cY)])
            cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
            cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        for j in points:
            d = (j[0] - x1) * (j[0] - x1) + (j[1] - y1) * (j[1] - y1)
            distances.append(d)
        if len(distances) == 0:
            print('no detected particle')
            return
        k = distances.index(min(distances))
        print(points[k])
        image = cv2.resize(image, (683, 680))
        cv2.imshow("Image", image)
        auto.move(260, 1057, 1, 1)
        cv2.waitKey(5000)
        p1 = points[k]
        return p1

    def handle_loaction(self):
        c = auto.get_point()
        x2 = int(c[0])
        y2 = int(c[1])
        print(x2, y2)
        auto.move(67, 1058, 0.5, 1)
        auto.move(515, 103, 2, 1)
        auto.move(453, 234, 2, 1)
        auto.move(370, 267, 2, 1)
        a = 535 + 5.77 * auto.get_X1()
        b = 962 - 5.77 * auto.get_Y1()
        A = 535 + 5.77 * auto.get_X1() + 5.77 * 0.083 * (x2 - x1)
        B = 962 - 5.77 * auto.get_Y1() + 5.77 * 0.083 * (y2 - y1)
        auto.move(476, 171, 2, 1)
        pyautogui.moveTo(a, b, duration=2)
        pyautogui.dragTo(A, B, 5, button='left')
        time.sleep(2)
        auto.move(398, 273, 2, 1)
        pyautogui.moveTo(903, 643, duration=2)
        pyautogui.dragTo(A, B, 5, button='left')
        time.sleep(1)
        auto.move(1787, 319, 2, 1)
        auto.delete_type()
        auto.move(463, 168, 2, 1)
        auto.move(43, 215, 1, 1)
        auto.move(119, 1056, 1, 1)
        auto.move(106, 246, 1, 1)
        auto.delete_type()
        time.sleep(185)
        auto.move(67, 1058, 0.5, 1)
        auto.move(397, 107, 0.5, 1)
        auto.move(227, 213, 0.5, 1)
        pyautogui.click()
        auto.move(119, 1056, 1, 1)
        auto.move(106, 246, 1, 1)
        auto.delete_type()
        auto.move(106, 246, 1, 1)
        auto.delete_type()

auto = Auto(10, 10, 10, 10)

if __name__ == '__main__':
    auto.handle_loaction()