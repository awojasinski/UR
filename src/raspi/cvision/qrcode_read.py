import cv2 as cv
import numpy as np
import time

def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv.line(im, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv.imshow("Results", im)

img = cv.imread('qr3.jpg')
qrDecoder = cv.QRCodeDetector()

data, bbox, rectifiedImg = qrDecoder.detectAndDecode(img)
if len(data)>0:
    print("Decoded Data : {}".format(data))
    display(img, bbox)
    rectifiedImage = np.uint8(rectifiedImg);
    cv.imshow("Rectified QRCode", rectifiedImg);
else:
    print("QR Code not detected")
    cv.imshow("Results", img)

cv.waitKey(0)
cv.destroyAllWindows()