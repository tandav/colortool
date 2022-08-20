__version__ = '0.0.6'

import colorsys
import random
import string

RGBInt = tuple[int, int, int]
RGBFloat = tuple[float, float, float]
HexColor = int


def minmax_scaler(value: float, oldmin: float, oldmax: float, newmin: float = 0.0, newmax: float = 1.0) -> float:
    '''
    >>> minmax_scaler(50, 0, 100, 0.0, 1.0)
    0.5
    >>> minmax_scaler(255, 0, 255, 0.0, 1.0)
    1.0
    '''
    return (value - oldmin) * (newmax - newmin) / (oldmax - oldmin) + newmin


def hex_to_rgb(color: HexColor) -> RGBInt:
    if not (0 <= color <= 0xFFFFFF):
        raise ValueError('color must be in range [0, 0xFFFFFF]')
    a, b, c = color.to_bytes(3, byteorder='big')
    return a, b, c


def rgb_to_hex(color: RGBInt) -> HexColor:
    return int.from_bytes(bytes(color), byteorder='big')


def rgba_to_rgb(rgb_background, rgba_color):
    """https://stackoverflow.com/a/21576659/4204843"""

    alpha = rgba_color[3]

    return (
        int((1 - alpha) * rgb_background[0] + alpha * rgba_color[0]),
        int((1 - alpha) * rgb_background[1] + alpha * rgba_color[1]),
        int((1 - alpha) * rgb_background[2] + alpha * rgba_color[2]),
    )


def random_rgb():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def random_rgba():
    return random.randrange(255), random.randrange(255), random.randrange(255), 255


def random_hex():
    return f"#{int.from_bytes(random.randbytes(3), 'little'):06x}"


def css_hex(color: int) -> str:
    return f'#{color:06X}'


def to_rgb_int(color: str) -> RGBInt:
    return (
        int(color[1:3], base=16),
        int(color[3:5], base=16),
        int(color[5:7], base=16),
    )


def to_rgb_float(color: RGBInt) -> RGBFloat:
    return (
        minmax_scaler(color[0], 0, 255),
        minmax_scaler(color[1], 0, 255),
        minmax_scaler(color[2], 0, 255),
    )


def hls_to_css_hex(h: float, l: float, s: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r = int(minmax_scaler(r, 0, 1, 0, 255))
    g = int(minmax_scaler(g, 0, 1, 0, 255))
    b = int(minmax_scaler(b, 0, 1, 0, 255))
    return f'#{r:02X}{g:02X}{b:02X}'


def font_color(color: str, threshold: float = 0.5) -> str:
    rgb = to_rgb_float(to_rgb_int(color))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return '#FFFFFF' if l < threshold else '#000000'


def lighter(color: str, ratio: float = 0.5) -> str:
    rgb = to_rgb_float(to_rgb_int(color))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return hls_to_css_hex(h, l + (1 - l) * ratio, s)


def darker(color: str, ratio: float = 0.5) -> str:
    rgb = to_rgb_float(to_rgb_int(color))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return hls_to_css_hex(h, l * ratio, s)


def font_border_colors(
    color: str,
    font_threshold: float = 0.5,
    border_threshold: float = 0.9,
) -> tuple[str, str]:
    """
    determine the font color to be either black or white depending on the background color
    https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/

    :param color: hex string in #4bb9ac format
    :param font_threshold: 0..1 float. lightness value below the threshold will result in white, any above will result in black
    :param border_threshold: 0..1 float. lightness value below the threshold will result the border-color as same, any above 30% darker shade of the same color
    :return: font_color, border_color in css hex string format #4bb9ac
    """
    rgb = to_rgb_float(to_rgb_int(color))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    border_color = color if l < border_threshold else hls_to_css_hex(h, l * 0.7, s)
    return font_color(color), border_color


def is_hex_color(v: str) -> bool:
    return v.startswith('#') and set(v[1:]) <= set(string.hexdigits)


class colors:
    WHITE_BRIGHT = 0xFFFFFF
    BLACK_BRIGHT = 0x000000
    MAGENTA = 0x4457e5
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x4f88ea
    RED_PALE = 0xe2c5c5
    GREEN_PALE = 0x8ccc96
    WHITE_PALE = 0xAAAAAA
    BLACK_PALE = 0x505050
    YELLOW = 0xe2ed1a
