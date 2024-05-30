from colorsys import rgb_to_hsv, hsv_to_rgb
class Preprocess_Pet_Image_Data():

    # RGB를 HSV로 변환
    def rgb_to_hsv_255(self, r, g, b):
        return tuple(int(i * 255) for i in rgb_to_hsv(r / 255, g / 255, b / 255))

    # HSV를 RGB로 변환
    def hsv_to_rgb_255(self, h, s, v):
        return tuple(int(i * 255) for i in hsv_to_rgb(h / 255, s / 255, v / 255))


