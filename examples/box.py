import axidraw

W, H = 14, 11
BOUNDS = axidraw.A3_BOUNDS


def main():
    paths = [
        [(0, 0), (W, 0), (W, H), (0, H), (0, 0)]
    ]
    d = axidraw.Drawing(paths)
    d = d.center(*BOUNDS[-2:])
    d.dump('box.axi')
    d.render(bounds=BOUNDS).write_to_png('box.png')


if __name__ == '__main__':
    main()
