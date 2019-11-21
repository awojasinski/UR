import cv2 as cv
from pyzbar import pyzbar
import numpy as np


def qrRecognition(image):
    barcodes = pyzbar.decode(image)

    shapes_info = np.empty(shape=(0, 2))

    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        print(x, ',', y, ',', w, ',', h)
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                   0.5, (0, 0, 255), 2)

        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        shapes_info = np.append(shapes_info, [[x, y], barcodeData])

    return shapes_info
