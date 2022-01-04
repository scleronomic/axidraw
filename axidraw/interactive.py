from pynput import keyboard
from axidraw.device import Device


def main():
    x = [0, 0]
    device = Device()
    # device.home()
    device.pen_up()
    device.pen_down()

    def on_press(key):
        try:
            key = key.char
        except AttributeError:
            pass

        dx, dy = 0, 0
        if key == keyboard.Key.right:
            dx = -0.1
        if key == keyboard.Key.left:
            dx = +0.1
        if key == keyboard.Key.up:
            dy = 0.1
        if key == keyboard.Key.down:
            dy = -0.1

        if key == 'u':
            device.pen_up()

        if key == 'j':
            device.pen_down()

        x[0] += dx
        x[1] += dy

        device.move(dx, dy)

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()
