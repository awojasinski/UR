import cv2 as cv
from matplotlib import pyplot as plt
from pyzbar import pyzbar

img = cv.imread('img/qr1.jpg')
scale_percent = 40 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv.resize(img, dim)
my_dpi = 60

barcodes = pyzbar.decode(img)
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

# show the output image
plt.figure(num=None, figsize=(dim[0]/my_dpi, dim[1]/my_dpi), dpi=my_dpi)
plt.imshow(img)
plt.show()
cv.waitKey(0)