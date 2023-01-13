import axidraw


TEXT = 'Hello World'
font = axidraw.Font(axidraw.FUTURAL, 14)
d = font.wrap(TEXT, 11.5, 1.5, justify=True)
d = d.center(12, 8.5)
d.render()

axidraw.draw(drawing=d)