from PIL import Image


def vertical_repeat(unit1: Image.Image, unit2: Image.Image, repeat_count: int) -> Image.Image:
    target_width = max(unit1.width, unit2.width)
    if unit1.width != target_width:
        unit1 = unit1.resize((target_width, int(unit1.height * target_width / unit1.width)), Image.Resampling.LANCZOS)
    if unit2.width != target_width:
        unit2 = unit2.resize((target_width, int(unit2.height * target_width / unit2.width)), Image.Resampling.LANCZOS)
    seq = [unit1.copy() if i % 2 == 0 else unit2.copy() for i in range(repeat_count)]
    canvas = Image.new("RGB", (target_width, sum(i.height for i in seq)), "white")
    y = 0
    for s in seq:
        canvas.paste(s, (0, y)); y += s.height
    return canvas
