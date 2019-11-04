import cv2 as cv
import imutils
import numpy as np
from matplotlib import pyplot as plt

# colors in Hue Saturation Value color space
colors = {
    'red': np.array([0, 100, 100]),
    'orange': np.array([30, 100, 100]),
    'yellow': np.array([60, 100, 100]),
    'green': np.array([120, 100, 100]),
    'blue': np.array([240, 100, 100]),
    'violet': np.array([270, 100, 100]),
    'pink': np.array([330, 100, 100]),
}

def rgb_to_hsv(pixelRGB):
    r, g, b = pixelRGB / 255.0

    cmax = max(r, b, g)
    cmin = min(r, b, g)
    diff = cmax-cmin

    if cmax == cmin:
        h = 0

    elif cmax == r:
        h = (60 * (((g - b) / diff) % 6))

    elif cmax == g:
        h = (60 * (((b - r) / diff) + 2))

    elif cmax == b:
        h = (60 * (((r - g) / diff) + 4))

    if cmax == 0:
        s = 0;
    else:
        s = (diff / cmax) * 100

    v = cmax * 100
    return [int(h), int(s), int(v)]

def colorRecognition(pixelRGB):
    pixelHSV = rgb_to_hsv(pixelRGB)
    if pixelHSV[1] < 10:
        if pixelHSV[2] < 12:
            return 'black'
        elif pixelHSV[2] > 80:
            return 'white'
        else:
            return 'gray'
    else:
        diff = np.empty(shape=(0, 2), dtype=([('values', np.dtype(int)), ('names', type(colors.keys()))]))

        for name, value in colors.items():
            abs_diff = abs(int(pixelHSV[0]) - int(value[0]))
            diff = np.append(diff, np.array([(abs_diff, name)], dtype=diff.dtype))
        color = np.sort(diff)[0][1]
        if pixelHSV[2] < 10:
            return 'black'
        else:
            return color


img = cv.imread('img/shapes_and_colors.jpg')
rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
blurred = cv.GaussianBlur(gray, (5, 5), 0)
thresh = cv.threshold(blurred, 70, 255, cv.THRESH_BINARY)[1]

cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

points = np.empty(shape=(0, 4))

for c in cnts:
    M = cv.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    #rgb_value = rgb.copy()
    #rgb_value = np.mean(np.mean(rgb[cX-2:cX+2, cY-2:cY+2], axis=0), axis=0)
    points = np.append(points, [[cX, cY, rgb[cX, cY], colorRecognition(rgb[cX, cY])]], axis=0)

    # cv.drawContours(img, [c], -1, (0, 0, 255), 2, cv.LINE_AA)

for c in range(len(points)):
    print(str(c+1)+'.'+'X: '+str(points[c][0])+', Y:'+str(points[c][1])+'\ncolor: '+points[c][3] + '\nrbg: '+str(points[c][2])+'\nhsv: '+str(rgb_to_hsv(points[c][2]))+'\n')
    # cv.rectangle(img, (points[c][0]-3, points[c][1]-3), (points[c][0]+3, points[c][1]+3), (255, 255, 255))
    cv.putText(img, str(c+1)+points[c][3], tuple([points[c][0], points[c][1]]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)


plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.show()
cv.waitKey(0)
cv.destroyAllWindows()
