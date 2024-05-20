import time
import cv2
import numpy as np
import imutils
from mss import mss

template = cv2.imread("fass_canticle2.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 10, 250)
#template = cv2.findContours(template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#(h, w) = template.shape[:2]
cv2.imshow("aa", template)

cv2.waitKey()