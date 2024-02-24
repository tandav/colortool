from __future__ import annotations

import colorsys
import functools
import random
import string
import typing as tp

__version__ = '0.6.0'

Float3 = tp.Tuple[float, float, float]
Float4 = tp.Tuple[float, float, float, float]
Int3 = tp.Tuple[int, int, int]
Int4 = tp.Tuple[int, int, int, int]
Int3Float = tp.Tuple[int, int, int, float]


class Color:
    def __init__(self, color: int, alpha: float | None = None):
        self.color = color
        self.alpha = alpha

    @property
    def color(self) -> int:
        return self._color

    @color.setter
    def color(self, color: int) -> None:
        if not 0 <= color <= 0xFFFFFF:
            raise ValueError('color must be in range [0, 0xFFFFFF]')
        self._color = color

    @color.getter
    def color(self) -> int:
        return self._color

    @property
    def alpha(self) -> float | None:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: float | None) -> None:
        if alpha is not None and not 0 <= alpha <= 1:
            raise ValueError('alpha must be in range [0, 1]')
        self._alpha = alpha

    @alpha.getter
    def alpha(self) -> float | None:
        return self._alpha

    def __str__(self) -> str:
        if self.alpha is None:
            return f'0x{self.color:06X}'
        return f'0x{self.color:06X}{int(self.alpha * 255):02X}'

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
        if not (len(color) == 7 and color.startswith('#') and set(color[1:]) <= set(string.hexdigits)):
            raise ValueError('color must be in #4bb9ac format')
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

        br, bg, bb = background._rgb_float
        r, g, b = color._rgb_float

        return cls.from_rgb_float((
            (1 - color.alpha) * br + color.alpha * r,
            (1 - color.alpha) * bg + color.alpha * g,
            (1 - color.alpha) * bb + color.alpha * b,
        ))

    @functools.cached_property
    def hex(self) -> int:
        return self.color

    @functools.cached_property
    def _css_hex(self) -> str:
        return f'#{self.color:06X}'

    @functools.cached_property
    def _css_hex_alpha(self) -> str:
        if self.alpha is None:
            raise ValueError('alpha is None')
        return f'#{self.color:06X}{int(self.alpha * 255):02X}'

    @functools.cached_property
    def css_hex(self) -> str:
        if self.alpha is None:
            return self._css_hex
        return self._css_hex_alpha

    @functools.cached_property
    def _rgb_int(self) -> Int3:
        r, g, b = self.color.to_bytes(3, byteorder='big')
        return r, g, b

    @functools.cached_property
    def _rgba_int(self) -> Int4:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self.color.to_bytes(3, byteorder='big')
        return r, g, b, int(self.alpha * 255)

    @functools.cached_property
    def rgb_int(self) -> Int3 | Int4:
        if self.alpha is None:
            return self._rgb_int
        return self._rgba_int

    @functools.cached_property
    def _rgb_float(self) -> Float3:
        r, g, b = self._rgb_int
        return r / 255, g / 255, b / 255

    @functools.cached_property
    def _rgba_float(self) -> Float4:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self._rgb_int
        return r / 255, g / 255, b / 255, self.alpha

    @functools.cached_property
    def rgb_float(self) -> Float3 | Float4:
        if self.alpha is None:
            return self._rgb_float
        return self._rgba_float

    @functools.cached_property
    def _rgba_int_float(self) -> Int3Float:
        if self.alpha is None:
            raise ValueError('alpha is None')
        r, g, b = self._rgb_int
        return r, g, b, self.alpha

    @functools.cached_property
    def _css_rgb(self) -> str:
        return f'rgb{self._rgb_int}'

    @functools.cached_property
    def _css_rgba(self) -> str:
        if self.alpha is None:
            raise ValueError('alpha is None')
        return f'rgba{self._rgba_int_float}'

    @functools.cached_property
    def css_rgb(self) -> str:
        if self.alpha is None:
            return self._css_rgb
        return self._css_rgba

    @functools.cached_property
    def hsl(self) -> Float3:
        h, l, s = colorsys.rgb_to_hls(*self._rgb_float)
        return round(h, 14), round(s, 14), round(l, 14)

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
        h, s, l = self.hsl  # pylint: disable=unused-variable
        return Color(0xFFFFFF) if l < threshold else Color(0x000000)

    def font_border_colors(
        self,
        font_threshold: float = 0.5,
        border_threshold: float = 0.9,
    ) -> tp.Tuple[Color, Color]:
        """
        determine the font color to be either black or white depending on the background color
        https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/

        :param color: hex string in #4bb9ac format
        :param font_threshold: 0..1 float. lightness value below the threshold will result in white, any above will result in black
        :param border_threshold: 0..1 float. lightness value below the threshold will result the border-color as same, any above 30% darker shade of the same color
        :return: font_color, border_color in css hex string format #4bb9ac
        """
        h, s, l = self.hsl
        border_color = self if l < border_threshold else Color.from_hsl((h, s, l * 0.7))
        return self.font_color(font_threshold), border_color

    def _repr_svg_(self) -> str:
        font_color = self.font_color()
        return f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="30">
            <rect width="100" height="30" fill="{self.css_hex}"/>
            <text
                x=50
                y=15
                font-size=14
                dominant-baseline="middle"
                text-anchor="middle"
                font-family="monospace"
                fill="{font_color.css_hex}"
            >{self}</text>'
        </svg>
        '''
