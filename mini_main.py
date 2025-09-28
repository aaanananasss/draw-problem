from PIL import Image, ImageDraw, ImageFont

base_img = Image.new("RGBA", (100, 100), (0, 255, 0))
txt = 'Sample <del color=red>text<del>'
rotate = 120
font = ImageFont.load_default(12)
SS = 4

temp_draw = ImageDraw.Draw(Image.new("RGBA", (max(1, int(0 * SS)), max(1, int(0 * SS))),(0, 0, 0, 0)))

bbox = temp_draw.textbbox((0, 0), txt, font)
txt_w, txt_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

temp_img = Image.new("RGBA", (max(1, int(txt_w * SS)), max(1, int(txt_h * SS))), (0, 0, 0, 0))
temp_draw = ImageDraw.Draw(temp_img)

temp_draw.text((0, 0), txt, (0, 0, 0), font)

if 0 <= rotate <= 360:
    temp_img = temp_img.rotate(-rotate, expand=True, resample=Image.BICUBIC)
    b = temp_img.getbbox()
    w, h = temp_img.size

    if 0 <= rotate <= 90:
        x0 = -b[0]
        y0 = -b[1]
    elif 90 < rotate <= 180:
        x0 = -b[0]
        y0 = -b[1]
    elif 180 < rotate <= 270:
        x0 = -(w - b[2])
        y0 = -(h - b[3])
    elif 270 < rotate < 360:
        x0 = -b[0]
        y0 = -(h - b[3])

base_img.paste(temp_img, (x0, y0), temp_img)
base_img.show()
