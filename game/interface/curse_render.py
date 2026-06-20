import curses
import time
from interface.inputs import get_input
from interface.render import render
from interface.update_marker import update_marker
#from world.map import generate_map
from simulation.update_world.update_map import Map,get_layer
from interface.navigate_menu import navigate_menu
from interface.update_center import update_center
from simulation.update_world.update_time import game_time




import random
import numpy as np














layer0,layer1,layer2=get_layer()

menu_items = ["Description", "Follow", "Inventory", "Skills", "Quit"]


# menu_items=["New Game","Load Game","Options","Quit"]


def Map_win(win):
    # layer_0_part=np.array(layer0)[Map.marker_pos[1]-5:Map.marker_pos[1]+5,Map.marker_pos[0]-5:Map.marker_pos[0]+5]
    # layer_1_part=np.array(layer1)[Map.marker_pos[1]-5:Map.marker_pos[1]+5,Map.marker_pos[0]-5:Map.marker_pos[0
    # ]+5]
    # layer_2_part=np.array(layer2)[Map.marker_pos[1]-5:Map.marker_pos[1]+5,Map.marker_pos[0]-5:Map.marker_pos[0]+5]
    win.clear()
    win.border()
    render_map=render(10,10,layer0,layer1,layer2,Map.marker_pos)
    for i in range(len(render_map)):
        win.addstr(i+1,1,render_map[i])

    win.addstr(12,1,f"centre at {Map.marker_pos}")
    win.addstr(13,1,f"marker at {Map.marker_pos}")
    
    
    win.refresh()
















def Main_menu(
    win,
):
    pass


def Time_win(win):
    win.clear()
    win.border()
    win.addstr(1,1,f"Time {game_time.hour}:{game_time.min} Day {game_time.day} Month {game_time.month} Year {game_time.year}")
    win.refresh()
    


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

map_win_edit=True
selected =0
def main(stdscr):
    global map_win_edit,selected
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    h, w = stdscr.getmaxyx()

    char_width = max(20, w // 4)
    map_width = w - char_width

    map_win = curses.newwin(h, map_width, 0, 0)
    char_win = curses.newwin(h, char_width, 0, map_width)
    time_win= curses.newwin(3,map_width,h-3,0)
    
    # menu_win=curses.newwin(10,10,0,10)
    stdscr.nodelay(1)
    stdscr.timeout(1000)
    
    
    key = stdscr.getch()
    key=get_input(key)
    if key=="switch":
        map_win_edit=not map_win_edit


    if key in {"ctrl up","ctrl down","ctrl left","ctrl right"}:
        update_center(key,Map)
        
        
        
    if map_win_edit:
            update_marker(key,Map)


    else:
        
        selected=navigate_menu(key,selected,len(menu_items))
    Map_win(map_win)
    Time_win(time_win)
        
    Char_menu(stdscr, char_win,selected)

        #time.sleep(0.1)



def render_sim():
    curses.wrapper(main)

if __name__ == "__main__":
    render_sim()
