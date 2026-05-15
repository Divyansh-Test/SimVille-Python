import time
from world.Map import generate_map
from interface.render import render
from interface.get_info import get_info
from world.creature import Creature
from ai.pathfinding import pathfinding
from simulation.govia import govia
import numpy as np
import curses

HEIGHT = 20
WIDTH = 20

marker = (0, 0)
end = [2, 4]


layer0, layer1, layer2 = generate_map(HEIGHT, WIDTH)

agent1 = Creature(
    "agent1",
    801,
    "a human",
    '@',
    100,
    100,
    [],
    0,
    0
)

layer2[0][0] = agent1.id

path = pathfinding(
    layer0,
    (agent1.x, agent1.y),
    (4, 4)
)


def main(stdscr):

    global marker
    global end
    global path
    global agent1 
    
    
    curses.curs_set(0)

    stdscr.nodelay(True)

    while True:
        
        

        stdscr.clear()

        h, w = stdscr.getmaxyx()

        # update target/path
        if len(path)==0:

            end = np.random.randint(1, 19, size=(2,)).tolist()

            path = pathfinding(
                layer0,
                (agent1.x, agent1.y),
                tuple(end)
            )

        # move agent
        else:
            
            x,y=govia(path, agent1)
            layer2[agent1.x][agent1.y] = -1
            agent1.x = x
            agent1.y = y
            layer2[agent1.x][agent1.y] = agent1.id

        # render map
        rows = render(
            marker,
            range(HEIGHT),
            range(WIDTH),
            layer0,
            layer1,
            layer2
        )

        for i, row in enumerate(rows):

            if i < h:
                stdscr.addstr(i, 0, str(row)[:w-1])

        # info panel
        info = get_info(
            layer0,
            layer1,
            layer2,
            marker[0],
            marker[1]
        )

        info_x = WIDTH * 4 + 2

        info_lines = [
            f"layer0: {info['layer0']}",
            f"layer1: {info['layer1']}",
            f"layer2: {info['layer2']}",
            f"agent: ({agent1.x}, {agent1.y})",
            f"target: {end}"
        ]

        for i, line in enumerate(info_lines):

            y = i

            if y < h and info_x < w:
                stdscr.addstr(y, info_x, line[:w - info_x - 1])

        

        # input
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

        
        stdscr.refresh()
        time.sleep(0.5)


curses.wrapper(main)