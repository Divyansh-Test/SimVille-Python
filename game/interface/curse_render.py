import curses
import time
from inputs import get_input
from render import render


menu_items = ["Description", "Follow", "Inventory", "Skills", "Quit"]


# menu_items=["New Game","Load Game","Options","Quit"]


def Map_win(win):
    win.clear()
    win.border()
    win.addstr(1, 1, "Map")
    win.refresh()


def Main_menu(
    win,
):
    pass


def Char_menu(stdscr, win, selected):
    win.clear()
    win.border()
    

    for i in range(len(menu_items)):
        if selected == i:
            stdscr.attron(curses.color_pair(1))
            
            win.addstr(i + 1, 1, menu_items[i],curses.color_pair(1))
            stdscr.attroff(curses.color_pair(1))
            
        else:
            win.addstr(i + 1, 1, menu_items[i])

    

    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    h, w = stdscr.getmaxyx()
    map_win = curses.newwin(10, 10, 0, 0)
    char_win = curses.newwin(10, 10, 0, 10)
    curses.napms(1000)
    # menu_win=curses.newwin(10,10,0,10)
    stdscr.nodelay(1)
    selected =0
    while True:
        key = stdscr.getch()
        key=get_input(key)
        
        
        if key == "down":
            selected += 1
        elif key == "up":
            selected -= 1

        map_win.addstr(1, 1,key)

        selected = selected % len(menu_items)

        map_win.refresh()
        Char_menu(stdscr, char_win,selected)
        stdscr.getch()
        time.sleep(1)


if __name__ == "__main__":
    curses.wrapper(main)
