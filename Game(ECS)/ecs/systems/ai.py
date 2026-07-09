from ecs.components.job import Job

class AISystem:
   def __init__(self,world,map):
      self.world=world
      self.map=map

   def update(self):
     self.world.add_component(52,Job({"Type":"Gather","Target":5}))
     self.world.add_component(51,Job({"Type":"Gather","Target":35}))
     # self.world.add_component(54,Job({"Type":"Gather","Target":7}))