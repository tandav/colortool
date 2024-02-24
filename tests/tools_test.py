import pytest

from colortool import Color

WHITE = Color(0xFFFFFF)
BLACK = Color(0x000000)
TEST_COLOR = Color(0xFA972E)


@pytest.mark.parametrize(
    ('background', 'color', 'alpha', 'expected'), [
        (0x9AEA8A, 0x9A008A, 0.45, 0x9A808A),
        (0x0B38FF, 0xFFFF0E, 0.4, 0x6C879E),
    ],
)
def test_from_background_and_color_alpha(background, color, alpha, expected):
    assert Color.from_background_and_color_alpha(
        Color(background),
        Color(color, alpha),
    ) == Color(expected)


@pytest.mark.parametrize(
    ('color', 'expected'), [
        (Color(0xFA972E), BLACK),
        (Color(0xFDE1C3), BLACK),
        (Color(0x673603), WHITE),
        (Color(0x904C04), WHITE),
    ],
)
def test_font_color(color, expected):
    assert color.font_color() == expected


@pytest.mark.parametrize(
    ('color', 'ratio', 'expected'), [
        (TEST_COLOR, 1, WHITE),
        (TEST_COLOR, 0.5, Color(0xFCCB96)),
    ],
)
def test_lighter(color, ratio, expected):
    assert color.lighter(ratio) == expected


@pytest.mark.parametrize(
    ('color', 'ratio', 'expected'), [
        (TEST_COLOR, 0, BLACK),
        (TEST_COLOR, 0.5, Color(0x904C03)),
    ],
)
def test_darker(color, ratio, expected):
    assert color.darker(ratio) == expected
