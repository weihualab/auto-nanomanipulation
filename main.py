from skimage import measure
import numpy as np
import imutils
from imutils import contours
import cv2
import pyautogui
import time

# get the position of tip on mosaic
print("---input x position on mosaic---")
mosaic_x = int(input())
print("---input y position on mosaic---")
mosaic_y = int(input())

# get the position of tip on nova
print("---input x position on nova---")
nova_x = int(input())
print("---input y position on nova---")
nova_y = int(input())


def get_position():
    time.sleep(5)
    try:
        for i in range(5):
            # Get and print the mouse coordinates.
            x, y = pyautogui.position()
            position = 'position（X,Y）is：{},{}'.format(str(x).rjust(4), str(y).rjust(4))
            pix = pyautogui.screenshot().getpixel((x, y))
            position += ' RGB:(' + str(pix[0]).rjust(3) \
                        + ',' + str(pix[1]).rjust(3) + ',' \
                        + str(pix[2]).rjust(3) + ')'
            print(position)
    except:
        print('***getting position failed***')
        time.sleep(0.5)


def delete_write(param, sleep_time):
    for i in range(6):
        pyautogui.press('Delete')
    pyautogui.typewrite(param)
    time.sleep(sleep_time)
    pyautogui.press('Enter')


def move_click(x, y, dur, sleep_time, position):
    pyautogui.moveTo(x, y, duration=dur)
    pyautogui.click()
    print('current position:', position)
    time.sleep(sleep_time)


def get_point():
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
        labelMask[labels == label] = 255400
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
        xInArea = 1460 >= cX >= 480
        yInArea = 1160 >= cY >= 240
        if xInArea and yInArea:
            points.append([int(cX), int(cY)])
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    for j in points:
        d = (j[0] - mosaic_x) * (j[0] - mosaic_x) + (j[1] - mosaic_y) * (j[1] - mosaic_y)
        distances.append(d)
    if len(distances) == 0:
        print('***no detected particles***')
        raise Exception
    selected_index = distances.index(min(distances))
    image = cv2.resize(image, (683, 680))
    cv2.imshow("particles", image)
    pyautogui.moveTo(748, 1057, duration=1)
    pyautogui.click()
    cv2.waitKey(5000)
    selected = points[selected_index]
    return selected


def handle_location():
    move_click(300, 1056, 1, 1, 'mosaic')
    position = get_point()
    particle_x = int(position[0])
    particle_y = int(position[1])
    print('target position:', particle_x, particle_y)
    move_click(300, 1056, 1, 0, 'mosaic')
    move_click(106, 246, 1, 1, 'exp time')
    delete_write('10', 3)

    # move tip to target position
    move_click(67, 1058, 1, 1, 'nova')
    move_click(515, 103, 1, 1, 'Scanning')
    move_click(453, 234, 1, 1, 'area')
    move_click(370, 267, 1, 1, 'probe')
    from_x = 535 + 5.77 * nova_x
    from_y = 962 - 5.77 * nova_y
    to_x = 535 + 5.77 * nova_x + 5.77 * 0.083 * (particle_x - mosaic_x)
    to_y = 962 - 5.77 * nova_y + 5.77 * 0.083 * (particle_y - mosaic_y)
    move_click(476, 171, 1, 1, 'feedback')
    pyautogui.moveTo(from_x, from_y, duration=3)
    pyautogui.dragTo(to_x, to_y, 5, button='left')

    # set scan param
    time.sleep(2)
    move_click(398, 273, 1, 1, 'scan area')
    pyautogui.moveTo(903, 643, duration=2)
    pyautogui.dragTo(to_x, to_y, 5, button='left')
    time.sleep(1)
    move_click(1755, 323, 1, 1, 'scan param')
    delete_write('5.000', 1)
    move_click(1141, 170, 1, 1, 'BV')
    delete_write('-10', 1)

    # start scanning
    move_click(476, 171, 1, 1, 'feedback')
    move_click(43, 215, 1, 1, 'run')

    # back to mosaic
    move_click(300, 1056, 1, 1, 'mosaic')
    move_click(106, 246, 1, 1, 'exp time')
    delete_write('400', 3)

    # pick-up
    time.sleep(100)

    # place
    move_click(67, 1058, 1, 1, 'nova')
    move_click(742, 102, 1, 1, 'Litho')
    move_click(373, 170, 1, 1, 'SetPoint')
    delete_write('0.1', 1)
    move_click(159, 229, 1, 1, 'Action')
    delete_write('10', 1)
    move_click(14, 505, 1, 1, 'point')
    point_x = 410 + 5.63 * nova_x
    point_y = 992 - 5.64 * nova_y
    move_click(point_x, point_y, 1, 1, 'point')
    time.sleep(3)
    move_click(42, 204, 1, 1, 'run')
    for i in range(10):
        time.sleep(1)
        pyautogui.click()
    move_click(476, 171, 1, 1, 'feedback')

    # back to mosaic
    move_click(300, 1056, 1, 1, 'mosaic')
    move_click(106, 246, 1, 1, 'exp time')
    delete_write('10', 3)
    time.sleep(3)
    pyautogui.click()
    delete_write('400', 3)
    time.sleep(3)


if __name__ == '__main__':
    handle_location()
    pyautogui.alert(text='program end', title='alert', timeout=10*1000)