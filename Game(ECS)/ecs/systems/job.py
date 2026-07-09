from utils.pathfinding import pathfinding
from ecs.components.position import Position
from ecs.components.job import Job
from ecs.components.path import Path
from ecs.components.move_to import MoveTo
from ecs.components.state import State
from ecs.components.type import Type

from logger_config import get_logger
logger=get_logger(__name__)

class JobSystem:
   def __init__(self,world,map):
      self.world=world
      self.map=map

   def update(self):
     for entity in self.world.get_entity_with(Job):
        entity_job=self.world.get_component(entity,Job).job


        # logger.info(f"entity_job:{entity_job} and entity is {entity}")
        
        if entity_job["Type"]=="Gather":
            target_id=entity_job["Target"]
            target_cord=self.move_job(entity,target_id)
            self.world.add_component(entity,State(f"Gathering {self.world.get_component(target_id,Type).type}"))

            # logger.info(f"target:{target}")

            self.gather(entity,target_id,target_cord)




   def get_path(self,entity,dest):
      if self.world.has_component(entity,Path):
         return
      start=(self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)

      self.world.add_component(entity,Path(pathfinding(start,dest,self.map.terrain_layer)))
      # logger.info(f"path:{self.world.get_component(entity,Path).path}")



   def  gather(self,entity,target_id,target_cord):


      # self.world.add_component(entity,)

      # I think ki ye moveTo bekar hai Research karo
      if  (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
          self.world.remove_component(entity,MoveTo)
          self.world.remove_component(entity,Path)
          
          self.world.remove_component(entity,Job)
          self.world.add_component(entity,State("Static"))



   def move_job(self,entity,target):
      #This function will remove the line of code and also add path to the entity this will be only used by the jobs which needs to move somewhere.

      target=self.world.get_component(target,Position)
      target=(target.x,target.y)
      self.get_path(entity,target)
      self.world.add_component(entity,MoveTo(target[0],target[1]))
      return target


