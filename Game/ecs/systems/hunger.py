from ecs.components.hunger import Hunger
from logger_config import get_logger
logger=get_logger(__name__)

class  HungerSystem:
   def __init__(self,world):
      self.world=world

   def update(self):
      for entity in self.world.get_entity_with(Hunger):
         hunger=self.world.get_component(entity,Hunger)
         hunger.hunger-=3
         self.world.update_component(entity,hunger)
         #logger.info(f"Entity {entity} has hunger {self.world.get_component(entity,Hunger).hunger}")
