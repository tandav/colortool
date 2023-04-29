from colortool import Color
from colortool import Gradient


def test_gradient():
    colors = [0x845EC2, 0xD65DB1, 0xFF6F91, 0xFF9671, 0xFFC75F, 0xF9F871]
    colors = [Color(c) for c in colors]
    assert Gradient(colors)(0.0) == Color(0x845EC2)
