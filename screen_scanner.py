import time
import cv2
import numpy as np
import imutils
from mss import mss

WINDOW_SIZE = 10
TOLERANCE = 0.30
running_average_arr = [0.0] * WINDOW_SIZE

template = cv2.imread(".\\images\\fass4.png")
template = cv2.Canny(template, 50, 150)
(h, w) = template.shape[:2]
start_time = time.time()
mon = {"top": 0, "left": 2500, "width": 900, "height": 300}

with mss() as sct:
    while True:
        last_time = time.time()
        img = sct.grab(mon)
        img = np.array(img)
        edged = cv2.Canny(img, 50, 150)

        found = None

        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        running_average_arr.pop(0) 
        running_average_arr.append(maxVal)
        running_average = np.average(running_average_arr)

        if running_average > TOLERANCE:
            (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
            (endX, endY) = (int((maxLoc[0] + w)), int((maxLoc[1] + h)))
            cv2.rectangle(img, (startX, startY), (endX, endY), (180, 105, 255), 2)

        print('The loop took: {0}'.format(time.time() - last_time))
        print(f"Max Val: {maxVal} Max Loc: {maxLoc} running average: {running_average}" )

        cv2.imshow('test', np.array(img))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


