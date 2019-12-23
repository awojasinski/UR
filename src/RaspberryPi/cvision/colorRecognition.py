import numpy as np
import cv2 as cv
from cvision.colorspaceConversion import rgb2hsv, bgr2hsv


# colors in Hue Saturation Value color space
colors = {
    'red': np.array([0, 100, 100]),
    'orange': np.array([50, 100, 100]),
    'yellow': np.array([60, 100, 100]),
    'green': np.array([120, 100, 100]),
    'blue': np.array([240, 100, 100]),
    'violet': np.array([260, 100, 100]),
    'pink': np.array([330, 100, 100]),
    'red': np.array([360, 100, 100]),
}


def colorRecognition(image, cnt):
    b, g, r = cv.split(image)
    mask = np.zeros(b.shape, np.uint8)
    cnt = np.array(cnt).reshape((-1, 1, 2)).astype(np.int32)
    cv.drawContours(mask, [cnt], -1, 255, -1)
    b = cv.mean(b, mask=mask)
    g = cv.mean(g, mask=mask)
    r = cv.mean(r, mask=mask)

    hsv = bgr2hsv(int(b[0]), int(g[0]), int(r[0]))
    if hsv[1] < 10:
        if hsv[2] < 12:
            return 'black'
        elif hsv[2] > 80:
            return 'white'
        else:
            return 'gray'
    else:
        diff = np.empty(shape=(0, 2), dtype=([('values', np.dtype(int)), ('names', type(colors.keys()))]))

        for name, value in colors.items():
            abs_diff = abs(int(hsv[0]) - int(value[0]))
            diff = np.append(diff, np.array([(abs_diff, name)], dtype=diff.dtype))
        color = np.sort(diff)[0][1]
        if hsv[2] < 10:
            return 'black'
        else:
            return color
