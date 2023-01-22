from __future__ import annotations

import colorsys
import functools
import random
import string

__version__ = '0.3.0'

Float3 = tuple[float, float, float]
Float4 = tuple[float, float, float, float]
Int3 = tuple[int, int, int]
Int4 = tuple[int, int, int, int]
Int3Float = tuple[int, int, int, float]


def is_css_hex_color(v: str) -> bool:
    return len(v) == 7 and v.startswith('#') and set(v[1:]) <= set(string.hexdigits)


class Color:
    """
    supported formats:
    hex, css_hex, rgb_int, rgb_float, hls
    """

    def __init__(self, color: int, alpha: float | None = None):
        if not (0 <= color <= 0xFFFFFF):
            raise ValueError('color must be in range [0, 0xFFFFFF]')
        if alpha is not None and not (0 <= alpha <= 1):
            raise ValueError('alpha must be in range [0, 1]')
        self.color = color
        self.alpha = alpha

    def __repr__(self) -> str:
        if self.alpha is None:
            return f'Color(0x{self.color:06X})'
        return f'Color(0x{self.color:06X}, alpha={self.alpha})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return (self.color, self.alpha) == (other.color, other.alpha)

    def __hash__(self) -> int:
        return hash((self.color, self.alpha))

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
    def from_css_rgb(cls, color: str) -> Color:
        r, g, b = color[4:-1].split(',')
        return cls.from_rgb_int((int(r), int(g), int(b)))

    @classmethod
    def from_css_rgba(cls, color: str) -> Color:
        x = color[5:-1].split(',')
        return cls.from_rgba_int_float((int(x[0]), int(x[1]), int(x[2]), float(x[3])))

    @classmethod
    def from_rgb_int(cls, color: Int3) -> Color:
        return cls(int.from_bytes(bytes(color), byteorder='big'))

    @classmethod
    def from_rgba_int_float(cls, color: Int3Float) -> Color:
        return cls(int.from_bytes(bytes(color[:3]), byteorder='big'), color[3])

    @classmethod
    def from_rgba_int(cls, color: Int4) -> Color:
        return cls(int.from_bytes(bytes(color[:3]), byteorder='big'), color[3] / 255)

    @classmethod
    def from_rgba_float(cls, color: Float4) -> Color:
        return cls.from_rgba_int_float((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), color[3]))

    @classmethod
    def from_rgb_float(cls, color: Float3) -> Color:
        if not all(0 <= c <= 1 for c in color):
            raise ValueError('color must be in range [0, 1]')
        return cls.from_rgb_int((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    @classmethod
    def from_hsl(cls, hsl: Float3) -> Color:
        if not all(0 <= c <= 1 for c in hsl):
            raise ValueError('color must be in range [0, 1]')
        h, s, l = hsl
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return cls.from_rgb_float((r, g, b))

    @classmethod
    def from_background_and_color_alpha(
        cls,
        background: Color,
        color: Color,
    ) -> Color:
        """https://stackoverflow.com/a/21576659/4204843
        RGBA color on RGB background
        """
        if color.alpha is None:
            raise ValueError('color.alpha must not be None')

        if background.alpha is not None:
            raise ValueError('background color must not have alpha')

        br, bg, bb = background.rgb_float
        r, g, b = color.rgb_float

        return cls.from_rgb_float((
            (1 - color.alpha) * br + color.alpha * r,
            (1 - color.alpha) * bg + color.alpha * g,
            (1 - color.alpha) * bb + color.alpha * b,
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
    def rgba_int(self) -> Int4:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self.color.to_bytes(3, byteorder='big')
        return r, g, b, int(self.alpha * 255)

    @functools.cached_property
    def rgb_float(self) -> Float3:
        r, g, b = self.rgb_int
        return r / 255, g / 255, b / 255

    @functools.cached_property
    def rgba_float(self) -> Float4:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self.rgb_int
        return r / 255, g / 255, b / 255, self.alpha

    @functools.cached_property
    def rgba_int_float(self) -> Int3Float:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self.rgb_int
        return r, g, b, self.alpha

    @functools.cached_property
    def css_rgb(self) -> str:
        return f'rgb{self.rgb_int}'

    @functools.cached_property
    def css_rgba(self) -> str:
        if self.alpha is None:
            raise ValueError('alpha is None')
        return f'rgba{self.rgba_int_float}'

    @functools.cached_property
    def hsl(self) -> Float3:
        h, l, s = colorsys.rgb_to_hls(*self.rgb_float)
        return h, s, l

    def lighter(self, ratio: float = 0.5) -> Color:
        h, s, l = self.hsl
        return Color.from_hsl((h, s, l + (1 - l) * ratio))

    def darker(self, ratio: float = 0.5) -> Color:
        h, s, l = self.hsl
        return Color.from_hsl((h, s, l * ratio))

    def font_color(self, threshold: float = 0.5) -> Color:
        """
        determine the font color to be either black or white depending on the background color
        https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/

        :param threshold: 0..1 float. lightness value below the threshold will result in white, any above will result in black
        :return: font_color in css hex string format
        """
        h, s, l = self.hsl
        return WHITE_BRIGHT if l < threshold else BLACK_BRIGHT

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
        h, s, l = self.hsl
        border_color = self if l < border_threshold else Color.from_hsl((h, s, l * 0.7))
        return self.font_color(font_threshold), border_color


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
