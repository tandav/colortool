import itertools

import pytest

import colortool
from colortool import Color


@pytest.mark.parametrize('color', (-1, 0xFFFFFF + 1))
def test_range_validation(color):
    with pytest.raises(ValueError):
        Color(color)


def test_rgb_float_range_validation():
    with pytest.raises(ValueError):
        Color.from_rgb_float((1.1, 0, 0))


@pytest.mark.parametrize(
    'hex, css_hex, rgb_int, rgb_float, hsl', (
        (0x000000, '#000000', (0, 0, 0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        (0x0FACED, '#0FACED', (15, 172, 237), (0.058823529411764705, 0.6745098039215687, 0.9294117647058824), (0.5487987987987988, 0.8809523809523809, 0.49411764705882355)),
        (0xBADA55, '#BADA55', (186, 218, 85), (0.7294117647058823, 0.8549019607843137, 0.3333333333333333), (0.20676691729323307, 0.6425120772946858, 0.5941176470588235)),
    ),
)
def test_conversions(hex, css_hex, rgb_int, rgb_float, hsl):
    keys = 'hex', 'css_hex', 'rgb_int', 'rgb_float', 'hsl'
    kv = zip(keys, (hex, css_hex, rgb_int, rgb_float, hsl))

    for (from_k, from_v), (to_k, to_v) in itertools.permutations(kv, 2):
        if from_k == 'hsl':
            continue  # too hard to compare
        print(from_k, '->', to_k, from_v, '->', to_v)
        color = getattr(Color, f'from_{from_k}')(from_v)
        assert getattr(color, to_k) == to_v, f'{from_k} -> {to_k}'


@pytest.mark.parametrize(
    'background, color, color_alpha, expected', (
        (0x9AEA8A, 0x9A008A, 0.45, 0x9A808A),
        (0x0B38FF, 0xFFFF0E, 0.4, 0x6C879E),
    ),
)
def test_from_background_and_color_alpha(background, color, color_alpha, expected):
    assert Color.from_background_and_color_alpha(
        Color.from_hex(background),
        Color.from_hex(color),
        color_alpha,
    ) == Color.from_hex(expected)


@pytest.mark.parametrize(
    'color, expected', [
        (Color.from_hex(0xFA972E), colortool.BLACK_BRIGHT),
        (Color.from_hex(0xFDE1C3), colortool.BLACK_BRIGHT),
        (Color.from_hex(0x673603), colortool.WHITE_BRIGHT),
        (Color.from_hex(0x904C04), colortool.WHITE_BRIGHT),
    ],
)
def test_font_color(color, expected):
    assert color.font_color() == expected


TEST_COLOR = Color.from_hex(0xFA972E)


@pytest.mark.parametrize(
    'color, ratio, expected', [
        (TEST_COLOR, 1, colortool.WHITE_BRIGHT),
        (TEST_COLOR, 0.5, Color.from_hex(0xFCCB96)),
    ],
)
def test_lighter(color, ratio, expected):
    assert color.lighter(ratio) == expected


@pytest.mark.parametrize(
    'color, ratio, expected', [
        (TEST_COLOR, 0, colortool.BLACK_BRIGHT),
        (TEST_COLOR, 0.5, Color.from_hex(0x904C03)),
    ],
)
def test_darker(color, ratio, expected):
    assert color.darker(ratio) == expected


@pytest.mark.parametrize(
    'string, expected', (
        ('#FACADE', True),
        ('#000000', True),
        ('#00000', False),
        ('FACADEC', False),
        ('#RACADE', False),
    ),
)
def test_is_css_hex_color(string, expected):
    assert colortool.is_css_hex_color(string) == expected
