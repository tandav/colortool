from __future__ import annotations

import colorsys
import functools
import random
import string

__version__ = '0.1.0'

Float3 = tuple[float, float, float]
Float4 = tuple[float, float, float, float]
Int3 = tuple[int, int, int]


def is_str_hex_color(v: str) -> bool:
    return v.startswith('#') and set(v[1:]) <= set(string.hexdigits)


class Color:
    """
    supported formats:
    hex, css_hex, rgb_int, rgb_float, hls
    todo: rename hls to hsl
    """

    def __init__(self, color: int):
        if not (0 <= color <= 0xFFFFFF):
            raise ValueError('color must be in range [0, 0xFFFFFF]')
        self.color = color

    def __repr__(self) -> str:
        return f'Color(0x{self.color:06X})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self.color == other.color

    @classmethod
    def random(cls) -> Color:
        return cls(random.randint(0, 0xFFFFFF))

    @classmethod
    def from_hex(cls, color: int) -> Color:
        return cls(color)

    @classmethod
    def from_css_hex(cls, color: str) -> Color:
        return cls(int(color[1:], base=16))

    @classmethod
    def from_rgb_int(cls, color: Int3) -> Color:
        return cls(int.from_bytes(bytes(color), byteorder='big'))

    @classmethod
    def from_rgb_float(cls, color: Float3) -> Color:
        if not all(0 <= c <= 1 for c in color):
            raise ValueError('color must be in range [0, 1]')
        return cls.from_rgb_int((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    @classmethod
    def from_hls(cls, color: Float3) -> Color:
        if not all(0 <= c <= 1 for c in color):
            raise ValueError('color must be in range [0, 1]')
        r, g, b = colorsys.hls_to_rgb(*color)
        return cls.from_rgb_float((r, g, b))

    @classmethod
    def from_background_and_color_alpha(
        cls,
        background: Color,
        color: Color,
        color_alpha: float,
    ) -> Color:
        """https://stackoverflow.com/a/21576659/4204843
        RGBA color on RGB background
        """
        if not (0 <= color_alpha <= 1):
            raise ValueError('color_alpha must be in range [0, 1]')

        br, bg, bb = background.rgb_float
        r, g, b = color.rgb_float

        return cls.from_rgb_float((
            (1 - color_alpha) * br + color_alpha * r,
            (1 - color_alpha) * bg + color_alpha * g,
            (1 - color_alpha) * bb + color_alpha * b,
        ))

    @functools.cached_property
    def hex(self) -> int:
        return self.color

    @functools.cached_property
    def css_hex(self) -> str:
        return f'#{self.color:06X}'

    @functools.cached_property
    def rgb_int(self) -> Int3:
        r, g, b = self.color.to_bytes(3, byteorder='big')
        return r, g, b

    @functools.cached_property
    def rgb_float(self) -> Float3:
        r, g, b = self.rgb_int
        return r / 255, g / 255, b / 255

    @functools.cached_property
    def hls(self) -> Float3:
        return colorsys.rgb_to_hls(*self.rgb_float)

    def lighter(self, ratio: float = 0.5) -> Color:
        h, l, s = self.hls
        return Color.from_hls((h, l + (1 - l) * ratio, s))

    def darker(self, ratio: float = 0.5) -> Color:
        h, l, s = self.hls
        return Color.from_hls((h, l * ratio, s))

    def font_color(self, threshold: float = 0.5) -> Color:
        """
        determine the font color to be either black or white depending on the background color
        https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/

        :param threshold: 0..1 float. lightness value below the threshold will result in white, any above will result in black
        :return: font_color in css hex string format
        """
        h, l, s = self.hls
        return colors.WHITE_BRIGHT if l < threshold else colors.BLACK_BRIGHT

    def font_border_colors(
        self,
        font_threshold: float = 0.5,
        border_threshold: float = 0.9,
    ) -> tuple[Color, Color]:
        """
        determine the font color to be either black or white depending on the background color
        https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/

        :param color: hex string in #4bb9ac format
        :param font_threshold: 0..1 float. lightness value below the threshold will result in white, any above will result in black
        :param border_threshold: 0..1 float. lightness value below the threshold will result the border-color as same, any above 30% darker shade of the same color
        :return: font_color, border_color in css hex string format #4bb9ac
        """
        # rgb = to_rgb_float(to_rgb_int(color))
        # h, l, s = colorsys.rgb_to_hls(*rgb)
        h, l, s = self.hls
        border_color = self if l < border_threshold else Color.from_hls((h, l * 0.7, s))
        return self.font_color(font_threshold), border_color


class colors:
    WHITE_BRIGHT = Color.from_hex(0xFFFFFF)
    BLACK_BRIGHT = Color.from_hex(0x000000)
    MAGENTA = Color.from_hex(0x4457e5)
    RED = Color.from_hex(0xFF0000)
    GREEN = Color.from_hex(0x00FF00)
    BLUE = Color.from_hex(0x4f88ea)
    RED_PALE = Color.from_hex(0xe2c5c5)
    GREEN_PALE = Color.from_hex(0x8ccc96)
    WHITE_PALE = Color.from_hex(0xAAAAAA)
    BLACK_PALE = Color.from_hex(0x505050)
    YELLOW = Color.from_hex(0xE2ED1A)
