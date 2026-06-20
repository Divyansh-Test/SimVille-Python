def navigate_menu(key,selected,menu_len):
  if key == "down":
    selected += 1
  elif key == "up":
    selected -= 1



  selected = selected % menu_len

  return selected
  