from simulation.generate_map import generate_map


class WorldMap:
  def  __init__(self,width,height,seed=None):
     self.width=width
     self.height=height
     self.seed=seed
     self.layer0,self.layer1,self.layer2=generate_map(width,height,seed)
     self.marker_pos=(5,5)
     #self.centre_At=self.marker_pos

  def update_marker(self,dir):
     old=self.marker_pos
     if dir=="up":
        self.marker_pos=(self.marker_pos[0],self.marker_pos[1]-1)

     elif dir== "down":
        self.marker_pos=(self.marker_pos[0],self.marker_pos[1]+1)
     elif dir=="left":
        self.marker_pos=(self.marker_pos[0]-1,self.marker_pos[1])

     elif dir=="right":
        self.marker_pos=(self.marker_pos[0]+1,self.marker_pos[1])

     if self.marker_pos[0]<0 or self.marker_pos[0]>=self.width or self.marker_pos[1]<0 or self.marker_pos[1]>=self.height:
        self.marker_pos=old


  # def update_centre_point(self,dir):
  #       old=self.centre_At
  #       if dir=="ctrl up":
  #          self.centre_At=(self.centre_At[0],self.centre_At[1]-1)

  #       elif dir== "ctrl down":
  #          self.centre_At=(self.centre_At[0],self.centre_At[1]+1)
  #       elif dir=="ctrl left":
  #          self.centre_At=(self.centre_At[0]-1,self.centre_At[1])

  #       elif dir=="ctrl right":
  #          self.centre_At=(self.centre_At[0]+1,self.centre_At[1])

  #       if self.centre_At[0]<0 or self.centre_At[0]>=self.width or self.centre_At[1]<0 or self.centre_At[1]>=self.height:
  #          self.centre_At=old
       
    