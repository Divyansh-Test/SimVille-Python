from ecs.components.health import Health
from ecs.components.hunger import Hunger
from ecs.components.job import Job
from ecs.components.position import Position
from ecs.components.inventory import Inventory
from ecs.components.state import State
from ecs.components.type import Type
from ecs.components.renderable import Renderable
from ecs.components.path import Path
from ecs.components.move_to import MoveTo

class World:
  def __init__(self):
    self.next_entity_id=0
    self.components={
      Position:{},
      Health:{},
      Inventory:{},
      State:{},
      Job:{},
      Hunger:{},
      Type:{},
      Renderable:{},
      Path:{},
      MoveTo:{},
    }
    
  def create_entity(self):
    self.next_entity_id+=1
    return self.next_entity_id

  def update_component(self):
    pass  

  def remove_component(self,entity,component_type):
    if component_type not in self.components:
      # raise ValueError(f"Component type {component_type} not found in world")
      return None

    if entity not in self.components[component_type]:
      # raise ValueError(f"Entity {entity} does not have component {component_type}")
      return None

    del self.components[component_type][entity]
    return True

  def get_component(self,entity,component_type):
     if component_type not in self.components:
        # raise ValueError(f"Component type {component_type} not found in world")
        return None
     component=self.components[component_type].get(entity)
     return component


  def add_component(self,entity,*args):
    for component in args:
      component_type=type(component)
      self.components[component_type][entity]=component


  def has_component(self,entity,component_type):
    if component_type not in self.components:
      # raise ValueError(f"Component type {component_type} not found in world")
      return None

    if entity not in self.components[component_type]:
      return False

    return True
    

  def get_entity_with(self,*args):
    entities=[]
    for component_type in args:
      if component_type not in self.components:
        # raise ValueError(f"Component type {component_type} not found in world")
        return set()
      entities.append(set(self.components[component_type].keys()))

    if not entities:
      return set()

    return set.intersection(*entities)
    
    
    

  def destroy_entity(self,entity):
    for component_type in self.components.values():
      component_type.pop(entity,None)
      






if  __name__=="__main__":
  world=World()
  world.add_component(1,Position(10,29))
  # # for _ in range(10):
  # #   entity=world.create_entity()
  print(world.remove_component(1,Position))
  