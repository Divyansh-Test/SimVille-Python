import curses
import time
from inputs import get_input  
from render import render


menu_items=["Description","Follow","Inventory","Skills","Quit"]


#menu_items=["New Game","Load Game","Options","Quit"]


def Map_win(win):
  win.clear()
  win.border()
  win.addstr(1,1,"Map")
  win.refresh()
def Main_menu(win,):
  pass

def Char_menu(win,key):
  win.clear()
  win.border()
  win.addstr(1,1,"Char")
  win.refresh()






def main(stdscr):
  curses.curs_set(0)
  h,w=stdscr.getmaxyx()
  map_win=curses.newwin(10,10,0,0)
  char_win=curses.newwin(10,10,0,10)
  #menu_win=curses.newwin(10,10,0,10)
  stdscr.nodelay(1)
  while True:
    key=stdscr.getch()
    get_input(key)

    Map_win(map_win)
    Char_menu(char_win,key)
    stdscr.getch()

  time.delay(0.5)


if __name__=="__main__":
   curses.wrapper(main)

  
  
  