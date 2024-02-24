import itertools

import pytest

from colortool import Color


@pytest.mark.parametrize('color', [-1, 0xFFFFFF + 1])
def test_range_validation(color):
    with pytest.raises(ValueError):
        Color(color)


def test_rgb_float_range_validation():
    with pytest.raises(ValueError):
        Color.from_rgb_float((1.1, 0, 0))


@pytest.mark.parametrize(
    ('hex', '_css_hex', '_rgb_int', '_css_rgb', '_rgb_float', 'hsl'), [
        (0x000000, '#000000', (0, 0, 0), 'rgb(0, 0, 0)', (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        (0x0FACED, '#0FACED', (15, 172, 237), 'rgb(15, 172, 237)', (0.058823529411764705, 0.6745098039215687, 0.9294117647058824), (0.5487987987988, 0.88095238095238, 0.49411764705882)),
        (0xBADA55, '#BADA55', (186, 218, 85), 'rgb(186, 218, 85)', (0.7294117647058823, 0.8549019607843137, 0.3333333333333333), (0.20676691729323, 0.64251207729469, 0.59411764705882)),
    ],
)
def test_conversions(hex, _css_hex, _rgb_int, _css_rgb, _rgb_float, hsl):  # noqa: A002, PT019
    keys = 'hex', '_css_hex', '_rgb_int', '_css_rgb', '_rgb_float', 'hsl'
    kv = zip(keys, (hex, _css_hex, _rgb_int, _css_rgb, _rgb_float, hsl))

    for (from_k, from_v), (to_k, to_v) in itertools.permutations(kv, 2):
        from_k = from_k.lstrip('_')  # noqa: PLW2901
        if from_k == 'hsl':
            continue  # too hard to compare
        print(from_k, '->', to_k, from_v, '->', to_v)  # noqa: T201
        color = getattr(Color, f'from_{from_k}')(from_v)
        assert getattr(color, to_k) == to_v, f'{from_k} -> {to_k}'


@pytest.mark.parametrize(
    ('string', 'is_valid'), [
        ('#FACADE', True),
        ('#000000', True),
        ('#00000', False),
        ('FACADEC', False),
        ('#RACADE', False),
    ],
)
def test_from_css_hex_validation(string, is_valid):
    if is_valid:
        Color.from_css_hex(string)
        return
    with pytest.raises(ValueError):
        Color.from_css_hex(string)


def test_hashable():
    a = Color(0x000000)
    b = Color(0x000000)
    assert hash(a) == hash(b)
    assert {a, b} == {a}


def test_alpha_from():
    c = Color(0x00FF00, alpha=0.5)
    assert Color.from_rgba_int_float((0, 255, 0, 0.5)) == c
    a = Color.from_rgba_int((0, 255, 0, 128))
    assert a.color == c.color
    assert pytest.approx(a.alpha, abs=1e-2) == c.alpha
    assert Color.from_rgba_float((0.0, 1.0, 0.0, 0.5)) == c
    assert Color.from_css_rgba('rgba(0, 255, 0, 0.5)') == c


def test_alpha_to():
    c = Color(0x00FF00, alpha=0.5)
    assert c._rgba_int == (0, 255, 0, 127)
    assert c._rgba_float == (0.0, 1.0, 0.0, 0.5)
    assert c._rgba_int_float == (0, 255, 0, 0.5)
    assert c._css_rgba == 'rgba(0, 255, 0, 0.5)'
    assert c._css_hex_alpha == '#00FF007F'


def test_alpha_raises():
    with pytest.raises(ValueError):
        Color.from_rgba_int_float((0, 0, 0, 1.1))
    with pytest.raises(ValueError):
        Color.from_rgba_int_float((0, 0, 0, -0.1))
    with pytest.raises(ValueError):
        Color.from_rgba_int_float((0, 0, 0, 1.1))
    with pytest.raises(ValueError):
        Color.from_rgba_int_float((0, 0, 0, -0.1))
    c = Color(0x00FF00)
    with pytest.raises(ValueError):
        c._rgba_int
    with pytest.raises(ValueError):
        c._rgba_float
    with pytest.raises(ValueError):
        c._rgba_int_float
    with pytest.raises(ValueError):
        c._css_rgba


def test_setter_validation():
    c = Color(0x00FF00)
    with pytest.raises(ValueError):
        c.color = -1
    with pytest.raises(ValueError):
        c.alpha = -0.1


def test_auto():
    c = Color(0x00FF00)
    assert str(c) == '0x00FF00'
    assert c.css_rgb == 'rgb(0, 255, 0)'
    assert c.css_hex == '#00FF00'
    assert c.rgb_float == (0.0, 1.0, 0.0)
    assert c.rgb_int == (0, 255, 0)

    c = Color(0x00FF00, alpha=0.9)
    assert str(c) == '0x00FF00E5'
    assert c.css_rgb == 'rgba(0, 255, 0, 0.9)'
    assert c.css_hex == '#00FF00E5'
    assert c.rgb_float == (0.0, 1.0, 0.0, 0.9)
    assert c.rgb_int == (0, 255, 0, 229)
