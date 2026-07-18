from ecs.components.thrist import Thrist
class ThristSystem:
   def __init__(self,world):
      self.world=world

   def update(self):
      for entity in self.world.get_entity_with(Thrist):
         thrist=self.world.get_component(entity,Thrist)
         thrist.update(-1)