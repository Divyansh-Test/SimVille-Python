
import curses

def  get_input(key):
   if  key==curses.KEY_UP:
      return "up"
   elif key==curses.KEY_DOWN:
      return "down"
   elif key==curses.KEY_LEFT:
      return "left"
   elif key==curses.KEY_RIGHT:
      return "right"

   elif key==ord("\t"):
      return "switch"
   elif key==ord("q"):
      return "quit"
   elif key==ord("i"):
      return "inventory"
   elif key==ord(" "):
      return "space"
   elif key==ord("c"):
      return "char"
   elif key==ord("m"):
      return "menu"
   elif key==ord("s"):
      return "skills"
   elif key==ord("d"):
      return "description"
   elif key==ord("f"):
      return "follow"
   elif key==ord("n"):
      return "new"
   elif key==ord("l"):
      return "load"
   elif key==ord("o"):
      return "options"
   elif key==ord("q"):
      return "quit"

   elif key==575:
      return "ctrl up"

   elif key==534:
      return "ctrl down"

   elif key==569:
      return "ctrl right"

   elif key==554:
      return "ctrl left"

   
   else:
      return "none"