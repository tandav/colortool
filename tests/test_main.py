import pytest

import colortool


@pytest.mark.parametrize('hex_, rgb', [
    (0x000000, (0, 0, 0)),
    (0xFFFFFF, (255, 255, 255)),
    (0x8FED6C, (143, 237, 108)),
])
def test_hex_rgb(hex_, rgb):
    assert colortool.hex_to_rgb(hex_) == rgb
    assert colortool.rgb_to_hex(rgb) == hex_


@pytest.mark.parametrize('color, expected', [
    (0x7CCB11, '#7CCB11'),
    (0x000000, '#000000'),
    (0x0000FF, '#0000FF'),
    (0x0000FE, '#0000FE'),
    (0xFF0000, '#FF0000'),
])
def test_css_hex(color, expected):
    assert colortool.css_hex(color) == expected


WHITE = '#FFFFFF'
BLACK = '#000000'
TEST_COLOR = '#FA972E'

@pytest.mark.parametrize('color, expected', [
    ('#FA972E', BLACK),
    ('#FDE1C3', BLACK),
    ('#673603', WHITE),
    ('#904C04', WHITE),
])
def test_font_color(color, expected):
    assert colortool.font_color(color) == expected


@pytest.mark.parametrize('color, ratio, expected', [
    (TEST_COLOR, 1, WHITE),
    (TEST_COLOR, 0.5, '#FCCB96'),
])
def test_lighter(color, ratio, expected):
    assert colortool.lighter(color, ratio) == expected


@pytest.mark.parametrize('color, ratio, expected', [
    (TEST_COLOR, 0, BLACK),
    (TEST_COLOR, 0.5, '#904C03'),
])
def test_darker(color, ratio, expected):
    assert colortool.darker(color, ratio) == expected


def test_random_hex():
    assert colortool.is_hex_color(colortool.random_hex())
