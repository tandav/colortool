import pytest

from colortool import Color


@pytest.mark.parametrize(
    'color', [
        Color(0xFA972E),
        Color(0xFA972E, alpha=0.9),
    ],
)
def test_repr_svg(color):
    color._repr_svg_()
