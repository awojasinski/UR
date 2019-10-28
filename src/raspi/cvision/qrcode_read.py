import cv2 as cv
from pyzbar import pyzbar

img = cv.imread('img/qr2.jpg')

barcodes = pyzbar.decode(img)
for barcode in barcodes:
    # extract the bounding box location of the barcode and draw the
    # bounding box surrounding the barcode on the image
    (x, y, w, h) = barcode.rect
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

# show the output image
cv.imshow("Image", img)
cv.waitKey(0)