# draw-problem
Draw Module : Problem with offset when rotating text on an image (Pillow). 

Brief, truncated question:

main.py (here I draw)
```py
from Tool import Tool #drawing methods
from Canvas import Canvas
from Object import Text #text object

p = Canvas((100, 100), Color.green) #base canvas 100x100

#drawing text
Tool.draw(
    p.layers[0].draw, #base canvas
    Text('Sample <del color=red>text<del>', Text.Font(
        'minecraft.ttf',
        12,
    )),
    fg=Color.black,
    rotate=100, #there are problems here
)

p.show()
```

Tool.py (drawing tools)
```py
    @staticmethod
    def draw(
        drawable: Object | Image.Image | Layer, #what we draw the object on (layer/canvas)
        obj: Object, #our text object
        coords: Sequence[int] | int = None, #default - (0, 0)
        fg: Object | Color = None, #black
        rotate: int = 0, #100
        ...
    ):
        if isinstance(drawable, ImageDraw.ImageDraw):
            base_img = drawable.im
            if not isinstance(base_img, Image.Image): base_img = Image.frombytes(base_img.mode, base_img.size, base_img.tobytes())
        elif isinstance(drawable, Image.Image): base_img = drawable
        elif hasattr(drawable, 'draw'): base_img = drawable.draw
        w, h = (size, size) if isinstance(size, int) else (size or (0, 0))
        SS = 4
        # --- Overall, this has nothing to do with the matter, but to clear the fog ---
        temp_img: Image.Image = Image.new("RGBA", (max(1, int(w * SS)), max(1, int(h * SS))), (0, 0, 0, 0)) #temp canvas 
        temp_draw: ImageDraw.ImageDraw = ImageDraw.Draw(temp_img)
        # ---
...
        elif isinstance(obj, Text):
            if obj.font.file: font: FreeTypeFont = ImageFont.truetype(obj.font.file, obj.font.size)
            else: font: FreeTypeFont = ImageFont.load_default(obj.font.size)

            bbox = temp_draw.textbbox((0, 0), obj.content, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            

            temp_img = Image.new("RGBA", (max(1, int(text_w * SS)), max(1, int(text_h * SS))), (0, 0, 0, 0)) #text canvas
            temp_draw = ImageDraw.Draw(temp_img)

            temp_draw.text((0, 0), obj.content, fg, font)

            if rotate != 0:
                temp_img = temp_img.rotate(-rotate, expand=True, resample=Image.BICUBIC) #new canvas with rotated text
                b = temp_img.getbbox()
                w, h = temp_img.size
                print(w, h, b)
                
                # --- ! PART FOR FIX ! ---
                if 0 <= rotate <= 90:
                    #Everything works perfectly here!
                    x0 = -b[0]
                    y0 = -b[1]
                elif 90 < rotate <= 180: 
                    #I tried to do something here, even working with h&w, but it didn't work out, I only laid the foundation
                    x0 = -b[0] - 0 #Basically, everything works correctly here, but I need to subtract some number... I can't do this manually (set the value, for example: -80...)
                    y0 = -b[1]
                elif 180 < rotate <= 270:
                    #doesn't work 
                    x0 = -(w - b[2]) 
                    y0 = -(h - b[3])
                elif 270 < rotate < 360: 
                    #doesn't work
                    x0 = -b[0]
                    y0 = -(h - b[3])
                else: #logical 0-90
                    x0 = -b[0]
                    y0 = -b[1]
...
#Paste a canvas with rotated text onto the base canvas
        base_img.paste(temp_img, (int(x0), int(y0)), temp_img) #x0 and y0 are the insertion coordinates, which I think need to be adjusted
```

I left only the necessary part of the code (some of it may not be important for someone, but who knows...).

In short:
- There's a problem with text shifting when rotating.
- When the text rotates 0-90°, everything works fine. Otherwise, the text shifts somewhere, even extending beyond the image boundaries.
- The text itself rotates correctly; the problem is precisely the incorrect text positioning (the shift needs to be adjusted).

So far, it only works with the 0-90 degree branch. I also tweaked a few things, and it seems to be working almost perfectly for 91-180: y0 is definitely correct, but something else needs to be subtracted from x0...

[![example][1]][1]
[1]: https://i.sstatic.net/LhEviYod.webp
