import numpy as np
from simulation.map.generator import generate_terrain
class Map:
  def __init__(self,width,height):
     self.width=width
     self.height=height
     self.terrain_layer=generate_terrain(self.height,self.width)
     
    