import cv2 as cv


def drawElement(shape_info, position, img):
    s = "X= " + str(position[0]) + "mm (" + str(shape_info[0]) + "px)\nY= " + str(position[1]) + "mm (" + str(shape_info[1]) + "px)"

    cv.circle(img, (shape_info[1], shape_info[0]), 2, (255, 255, 255))
    cv.putText(img, s, (shape_info[1]+10, shape_info[0]+10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    return img
