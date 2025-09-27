from Tool import Tool
from Canvas import Canvas
from Color import Color
from Object import Text

p = Canvas((100, 100), Color.green)

Tool.draw(
    p.layers[0].draw,
    Text('Sample <del color=red>text<del>', Text.Font(
        'minecraft.ttf',
        12,
    )),
    fg=Color.black,
    rotate=120,
)

p.show()