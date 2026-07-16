from interface.render_map import render_map
from interface.render_ui import render_time,render_options

class RenderSystem:
   def __init__(self,world,terrain_layer,map_win,ui_win):
      self.world=world
      self.map_win=map_win
      self.ui_win=ui_win
      self.terrain_layer=terrain_layer


   def update(self):
      render_map(self.world,self.terrain_layer,self.map_win)
      # render_time(self.world,self.ui_win)
      # render_options(self.world,self.ui_win)