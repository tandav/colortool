# colortool
set of tools to work with different color formats

## install from [pypi](https://pypi.org/project/colortool/)
```shell
pip install colortool
```

## examples
```python
>>> from colortool import Color

```

### convert color to different formats
```python
>>> green = Color.from_hex(0x00FF00)
>>> green.css_hex
'#00FF00'
>>> green.rgb_int
(0, 255, 0)
>>> green.rgb_float
(0.0, 1.0, 0.0)
>>> green.hsl
(0.33333333333333, 1.0, 0.5)

```

### create color from different formats
```python
>>> Color.from_css_hex('#00FF00')
Color(0x00FF00)
>>> Color.from_rgb_int((0, 255, 0))
Color(0x00FF00)
>>> Color.from_rgb_float((0.0, 1.0, 0.0))
Color(0x00FF00)
>>> Color.from_hsl((0.3333333333333333, 1.0, 0.5))
Color(0x00FF00)

```

### rgba colors
```python
>>> Color.from_rgba_int_float((0, 255, 0, 0.5))
Color(0x00FF00, alpha=0.5)

>>> Color.from_rgba_int_float((0, 255, 0, 0.5)).css_rgb
'rgba(0, 255, 0, 0.5)'

```

```python
### convert RGBA color on RGB background to RGB color
>>> Color.from_background_and_color_alpha(
...     background=Color(0x00FF00),
...     color=Color(0x000000,alpha=0.5),
... )
Color(0x007F00)

```

### make color darker or lighter
```python
>>> green.darker(ratio=0.5) # lightness = lightness * ratio
Color(0x007F00)
>>> green.lighter(ratio=0.5) # lightness = lightness + (1 - lightness) * ratio
Color(0x7FFF7F)

```
###  [determine the font color to be either black or white depending on the background color](https://css-tricks.com/switch-font-color-for-different-backgrounds-with-css/)
```python
>>> white = Color(0xFFFFFF)
>>> black = Color(0x000000)
>>> white.font_color()
Color(0x000000)
>>> black.font_color()
Color(0xFFFFFF)
>>> green.font_color()
Color(0x000000)

```

### also return darker variation of color if it is really light (see same css-tricks article)
```python
>>> green.font_border_colors()
(Color(0x000000), Color(0x00FF00))

```
