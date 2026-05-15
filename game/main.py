from world.Map import generate_map
from interface.render import render
from interface.get_info import get_info

import curses

HEIGHT = 20
WIDTH = 20

marker = (0, 0)

layer0, layer1, layer2 = generate_map(HEIGHT, WIDTH)


def main(stdscr):

    global marker

    curses.curs_set(0)

    while True:

        stdscr.clear()

        rows = render(
            marker,
            range(HEIGHT),
            range(WIDTH),
            layer0,
            layer1,
            layer2
        )

        # draw map
        for i, row in enumerate(rows):
            stdscr.addstr(i, 0, row)

        # draw info
        info = get_info(
            layer0,
            layer1,
            layer2,
            marker[0],
            marker[1]
        )

        stdscr.addstr(
            HEIGHT +1,
            1,
            f"layer0:{info['layer0']} "
            f"layer1:{info['layer1']} "
            f"layer2:{info['layer2']}"
        )

        stdscr.refresh()

        key = stdscr.getch()

        y, x = marker

        if key == ord("w"):
            y -= 1

        elif key == ord("s"):
            y += 1

        elif key == ord("a"):
            x -= 1

        elif key == ord("d"):
            x += 1

        elif key == ord("q"):
            break

        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            marker = (y, x)


curses.wrapper(main)