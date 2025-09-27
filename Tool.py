from PIL.ImageFont import FreeTypeFont
from Layer import Layer
from Color import Color
from typing import Sequence
from Object import Object, Text
from PIL import Image, ImageDraw, ImageFont

class Tool:
    @staticmethod
    def draw(
        drawable: Object | Image.Image | Layer,
        obj: Object,
        size: Sequence[int] | int = None,
        coords: Sequence[int] | int = None,
        fg: Object | Color = None,
        rotate: int = 0,
    ):
        if isinstance(drawable, ImageDraw.ImageDraw):
            base_img = drawable.im
            if not isinstance(base_img, Image.Image): base_img = Image.frombytes(base_img.mode, base_img.size, base_img.tobytes())
        elif isinstance(drawable, Image.Image): base_img = drawable
        elif hasattr(drawable, 'draw'): base_img = drawable.draw
        else: raise TypeError("drawable must be an Image, ImageDraw.Draw, or an object with a `draw` attribute")

        w, h = (size, size) if isinstance(size, int) else (size or (0, 0))
        x0, y0 = (coords, coords) if isinstance(coords, int) else (coords or (0, 0))
        fg = tuple(fg) + (255,) if fg and len(fg) == 3 else fg

        SS = 4
        temp_img: Image.Image = Image.new("RGBA", (max(1, int(w * SS)), max(1, int(h * SS))), (0, 0, 0, 0))
        temp_draw: ImageDraw.ImageDraw = ImageDraw.Draw(temp_img)

        if isinstance(obj, Text):
            if obj.font.file: font: FreeTypeFont = ImageFont.truetype(obj.font.file, obj.font.size)
            else: font: FreeTypeFont = ImageFont.load_default(obj.font.size)

            bbox = temp_draw.textbbox((0, 0), obj.content, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            temp_img = Image.new("RGBA", (max(1, int(text_w * SS)), max(1, int(text_h * SS))), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)

            temp_draw.text((0, 0), obj.content, fg, font)

            if 0 <= rotate <= 360:
                temp_img = temp_img.rotate(-rotate, expand=True, resample=Image.BICUBIC)
                b = temp_img.getbbox()
                w, h = temp_img.size
                print(w, h, b)

                #NEED FIX
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