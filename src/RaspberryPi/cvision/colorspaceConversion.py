
def rgb2hsv(r, g, b):

    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    cmax = max(r, b, g)
    cmin = min(r, b, g)
    diff = cmax-cmin

    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * (((g - b) / diff) % 6))
    elif cmax == g:
        h = (60 * (((b - r) / diff) + 2))
    else:
        h = (60 * (((r - g) / diff) + 4))

    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100

    v = cmax * 100
    return [int(h), int(s), int(v)]


def bgr2hsv(b, g, r):

    b = b / 255.0
    g = g / 255.0
    r = r / 255.0

    cmax = max(r, b, g)
    cmin = min(r, b, g)
    diff = cmax-cmin

    if cmax == cmin:
        h = 0

    elif cmax == r:
        h = (60 * (((g - b) / diff) % 6))

    elif cmax == g:
        h = (60 * (((b - r) / diff) + 2))

    elif cmax == b:
        h = (60 * (((r - g) / diff) + 4))

    if cmax == 0:
        s = 0;
    else:
        s = (diff / cmax) * 100

    v = cmax * 100
    return [int(h), int(s), int(v)]