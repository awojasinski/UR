import cv2 as cv


def drawElement(shape_info, position, img):
    s = "X=" + str(round(position[0], 2)) + "m(" + str(shape_info[0][1]) + "px)\nY=" + str(round(position[1], 2)) + "m(" + str(shape_info[0][0]) + "px)"

    cv.circle(img, (shape_info[0][1], shape_info[0][0]), 2, (255, 255, 255))

    dy = 20
    for i, line in enumerate(s.split('\n')):
        cv.putText(img, line, (shape_info[0][1]+10, shape_info[0][0]+10+i*dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    return img
