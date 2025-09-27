from PIL import Image
from datetime import datetime
from typing import Sequence
from Layer import Layer
from Color import Color
from Object import Object
import os

class Canvas:
    def __init__(self,
        size: Sequence[int],
        bg: Object | Color
    ) -> None:
        self.size: Sequence[int] = size
        self.bg: Object = tuple(bg + [255] if len(bg) == 3 else bg)

        self.layers = []
        "List of canvas layers"
        self.layers.append(Layer(
            self.size,
            self.bg,
        ))

    def save(self,
        format: str,
        filepath: str = None
    ) -> None:

        img: Image = self.layers[0].draw

        if not filepath: filepath = f"untitled-{datetime.now():%Y%m%d-%H%M%S}.png"

        if os.path.isdir(filepath) or filepath.endswith(('/', '\\')) or not os.path.splitext(filepath)[1]:
            filepath = os.path.join(filepath, f"untitled-{datetime.now():%Y%m%d-%H%M%S}.png")

        ext: str = os.path.splitext(filepath)[1].lower()
        fmt: str = (format or ext.replace('.', '') or 'png').upper()

        img.save(filepath, format=fmt)

    def show(self): self.layers[0].draw.show()