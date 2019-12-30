import numpy as np


def findElement(object_config_info, shapes_info, areaError=0):
    ret = False
    index = 0

    # Przeszukanie tablicy znalezionych elementów pod względem pola powierzchni
    if 'area' in object_config_info:
        areaResult = np.where((shapes_info > object_config_info['area']-areaError) & (shapes_info < object_config_info['area']+areaError))
        areaResult = list(zip(areaResult[0], areaResult[1]))
        if len(areaResult) != 0:
            ret = True
            index = areaResult[0][0]

    # Przeszukanie tablicy znalezionych elementów pod względem koloru obiektu
    if 'color' in object_config_info:
        colorResult = np.where(shapes_info == np.array(object_config_info['color']))
        colorResult = list(zip(colorResult[0], colorResult[1]))
        print(colorResult)
        if len(colorResult) != 0:
            ret = True
            index = colorResult[0][0]

    # Sprawdzenie czy znaleziony element o danym polu powierzchni to ten sam co znaleziony przy wyszukiwaniu koloru
    if 'area' and 'color' in object_config_info and 'colorResult' in locals() and 'areaResult' in locals():
        if colorResult[0] == areaResult[0]:
            ret = True
            index = colorResult[0][0]
        else:
            ret = False
            index = 0

    return ret, index
