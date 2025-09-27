from PIL import Image

class Layer:
    def __init__(self,
        size: list = None,
        bg: str = None,
    ): self.draw = Image.new("RGBA", size, bg)