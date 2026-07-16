def render_time(world,ui_win):
  ui_win.clear()
  ui_win.border()
  ui_win.addstr(0,1,f"centre at {Map.marker_pos}")
  ui_win.addstr(0,1,f"marker at {Map.marker_pos}")
  ui_win.addstr(1,1,f"Time {game_time.hour}:{game_time.min} Day {game_time.day} Month {game_time.month} Year {game_time.year}")
  win.refresh()



def render_options(world,ui_win):
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