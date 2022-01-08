import sys

from axidraw.device import Device
from axidraw.drawing import Drawing


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        return
    command, args = args[0], args[1:]
    command = command.lower()
    if command == 'render':
        d = Drawing.load(args[0])
        d = d.rotate_and_scale_to_fit(12, 8.5, step=90)
        path = args[1] if len(args) > 1 else 'out.png'
        im = d.render()
        im.write_to_png(path)
        return
    device = Device()
    if command == 'zero':
        device.zero_position()

    elif command == 'home':
        device.home()

    elif command == 'up':
        device.pen_up()

    elif command == 'down':
        device.pen_down()

    elif command == 'on':
        device.enable_motors()

    elif command == 'off':
        device.disable_motors()

    elif command == 'move':
        dx, dy = map(float, args)
        device.move(dx, dy)

    elif command == 'goto':
        x, y = map(float, args)
        device.goto(x, y)

    elif command == 'draw':
        d = Drawing.load(args[0])
        device.draw(d)  # TODO

    else:
        pass


if __name__ == '__main__':
    main()
