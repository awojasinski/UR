import numpy as np


def findElement(object_config_info, shapes_info, areaError=0):
    areaResult = None
    colorResult = None
    ret = False
    index = 0

    if 'area' in object_config_info:
        areaResult = np.where((shapes_info > object_config_info['area']-areaError) & (shapes_info < object_config_info['area']+areaError))
        areaResult = list(zip(areaResult[0], areaResult[1]))
        if len(areaResult) != 0:
            ret = True
            index = areaResult[0]

    if 'color' in object_config_info:
        colorResult = np.where(shapes_info == np.array(object_config_info['color']))
        colorResult = list(zip(colorResult[0], colorResult[1]))
        if len(colorResult) != 0:
            ret = True
            index = colorResult[0]

    if 'area' and 'color' and len(colorResult) != 0 and len(areaResult) != 0 in object_config_info:
        if colorResult[0] == areaResult[0]:
            ret = True
            index = colorResult[0]
        else:
            ret = False
            index = 0

    return ret, index
