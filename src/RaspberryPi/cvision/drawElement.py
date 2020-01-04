import cv2 as cv


def drawElement(shape_info, position, img):
    # Łańcuch znaków przechowywujący współrzędne X i Y w przestrzenii robota i na obrazie
    s = "X=" + str(round((position[0]*1000), 2)) + "mm(" + str(shape_info[0][0]) + "px)\nY=" + str(round((position[1]*1000), 2)) + "mm(" + str(shape_info[0][1]) + "px)"

    cv.circle(img, (shape_info[0][0], shape_info[0][1]), 2, (255, 255, 255))    # Narysowanie kropki w punkcie centralnym

    dy = 20
    # Wypisanie łańcucha s
    for i, line in enumerate(s.split('\n')):
        cv.putText(img, line, (shape_info[0][0]+10, shape_info[0][1]+10+i*dy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    return img
