import numpy as np
from cvision.colorspaceConversion import rgb2hsv, bgr2hsv


# colors in Hue Saturation Value color space
colors = {
    'red': np.array([0, 100, 100]),
    'orange': np.array([35, 100, 100]),
    'yellow': np.array([60, 100, 100]),
    'green': np.array([120, 100, 100]),
    'blue': np.array([240, 100, 100]),
    'violet': np.array([260, 100, 100]),
    'pink': np.array([330, 100, 100]),
    'red': np.array([360, 100, 100]),
}


def colorRecognition(image, pixel):
    pixelBGR = image[pixel[0]][pixel[1]]
    pixelHSV = bgr2hsv(pixelBGR)
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
