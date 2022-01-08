import axi

def main():
    system = axidraw.LSystem({
        'A': 'A-B--B+A++AA+B-',
        'B': '+A-BB--B-A++A+B',
    })
    d = system.run('A', 5, 60)
    # system = axidraw.LSystem({
    #     'X': 'F-[[X]+X]+F[+FX]-X',
    #     'F': 'FF',
    # })
    # d = system.run('X', 6, 20)
    d = d.rotate_and_scale_to_fit(12, 8.5, step=90)
    # d = d.sort_paths()
    # d = d.join_paths(0.015)
    d.render(bounds=axidraw.V3_BOUNDS).write_to_png('out.png')
    axidraw.draw(d)

if __name__ == '__main__':
    main()
