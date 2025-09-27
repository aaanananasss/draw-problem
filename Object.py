from __future__ import annotations

class Object: pass

class UI(Object): pass

class Text(UI):
    def __init__(self,
        content: str = '',
        font: Font = None,
    ) -> None:
        self.content = content
        self.font = font

    class Font:
        def __init__(self,
            file: str,
            size: int = 12,
        ) -> None:
            self.file = file
            self.size = size
