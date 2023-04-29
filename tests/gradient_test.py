import pytest

from colortool import Color
from colortool import Gradient


@pytest.fixture
def gradient():
    _colors = [0x845EC2, 0xD65DB1, 0xFF6F91, 0xFF9671, 0xFFC75F, 0xF9F871]
    return Gradient([Color(c) for c in _colors])


@pytest.mark.parametrize(
    ('color', 'expected'), [
        (0.0, 0x845EC2),
        (0.2, 0xD65DB1),
        (0.4, 0xFF6F91),
        (0.6, 0xFF9671),
        (0.8, 0xFFC75F),
        (0.9, 0xFCDF68),
        (1.0, 0xF9F871),
    ],
)
def test_gradient(gradient, color, expected):
    assert gradient(color) == Color(expected)
