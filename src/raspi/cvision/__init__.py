from cvision.qr import qrRecognition
from cvision.area import areaRecognition
from cvision.color_area import color_areaRecognition

func_mapping = {
    'qr-recognition': qrRecognition,
    'area-recognition': areaRecognition,
    'color-and-area-recognition': color_areaRecognition,
}
