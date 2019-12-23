import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cvision as cvis

config, order, mtx, dist, T, areaRatio = cvis.configRead('config.json')
element = 0

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

    img = frame.array

    height, width = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    img = img[y:y+h, x:x+w]
    cv.imshow("Live", img)

    key = cv.waitKey()
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == 13:
        s = input('Nazwa zdjęcia: ')
        cv.imwrite(s+'.png', img)
    elif key == ord('c'):
        shapes_info = cvis.objectRecognition(img)
        print('---------------------')
        print(shapes_info)
        print('---------------------\n')
        ret, index = cvis.findElement(shapes_info, order[element])
        print('---------------------')
        print("ret value: ", ret)
        print('index: ', index)

        if ret:
            print('object info: ', shapes_info[index])
            pos = cvis.tranformPos(shapes_info[index][0], T)
            print('Robot position', pos)
            element = element + 1

            if element == len(order):
                element = 0
        
    rawCapture.truncate(0)