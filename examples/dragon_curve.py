import axidraw


from wzk import new_fig

fig, ax = new_fig()


def main(iteration):
    turtle = axidraw.Turtle()

    for i in range(1, 2 ** iteration):
        turtle.forward(1)
        if (((i & -i) << 1) & i) != 0:
            turtle.circle(-1, 90, 36)
        else:
            turtle.circle(1, 90, 36)

    drawing = turtle.drawing.rotate_and_scale_to_fit(11, 8.5, step=90)

    drawing.render(ax=ax)
    # axidraw.draw(drawing)


if __name__ == '__main__':
    main(10)
    main(12)
