from __future__ import annotations
from typing import Sequence

class Object:
    def __init__(self):
        """Абстрактный класс визуализации объектов."""
        pass

class UI(Object):
    """Полноценные UI-элементы."""

class Text(UI):
    def __init__(self,
        content: str = '',
        font: Font = None,
    ) -> None:
        """
        Текст.
        """
        self.content = content
        self.font = font

    class Font:
        def __init__(self,
            file: str,
            size: int = 12,
            styles: Sequence[str] | str = None,
            direction: str = 'lr',
            interval: Sequence[int, int] = 1, #интервал межбуквенный, межстрочный
            break_words: bool = False,
        ) -> None:
            """Шрифт текста."""
            self.file = file
            self.size = size
            self.styles = styles
            self.direction = direction
            self.interval = interval
            self.break_words = break_words