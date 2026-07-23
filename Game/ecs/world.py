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
from ecs.components.blueprint import Blueprint
from ecs.components.thrist import Thrist
from ecs.components.growth import Growth
from ecs.components.vision import Vision
from logger_config import get_logger
logger=get_logger(__name__)

class World:
  def __init__(self,width,height):
    self.width=width
    self.height=height
    self.next_entity_id=0
    self.tick=0
    self.position_to_entity={}
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
      Blueprint:{},
      Vision:{},
      
      Growth:{},
      Thrist:{},
    }
    
  def create_entity(self):
    self.next_entity_id+=1
    return self.next_entity_id

  def update_component(self,entity,*component):
    for comp in component:
      
      component_type=type(comp)
      if component_type not in self.components:
        raise ValueError(f"Component type {component_type} not found in world")

      if component_type==Position:
        self.position_to_entity[(comp.x,comp.y)]=self.position_to_entity.get((comp.x,comp.y),[]).append(entity)  
      if entity not in self.components[component_type]:
        self.add_component(entity,comp)
        continue
      # logger.info(f"Component {component_type} of entity {entity} updated and component is {(list(comp.__dict__.values())[0])}")
      self.components[component_type][entity].update(list(comp.__dict__.values())[0])
      

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
      if component_type == Position:
        self.position_to_entity[(component.x,component.y)]=[entity]
      self.components[component_type][entity]=component


  def has_component(self,entity,component_type):
    if component_type not in self.components:
      # raise ValueError(f"Component type {component_type} not found in world")
      return None
    #return True

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
    pos=self.get_component(entity,Position)
    
    for component_name,component_data in self.components.items():
      logger.info(f"Entity {entity} has position {pos.x},{pos.y}")
      if component_name==Position:
        self.position_to_entity[(pos.x,pos.y)].remove(entity)
      
      component_data.pop(entity,None)

  def find_nearest_entity(self,entity,type):
    entity_position=self.get_component(entity,Position)
    nearest_entity=None
    nearest_distance=float('inf')
    nearest_entity_list=self.get_component(entity,Vision).nearest_entities
    for Entity in nearest_entity_list :
      items=self.get_component(Entity,Inventory).items.get(type,0)
      if items>0 and self.get_component(Entity,Type).type!="Human":
        nearest_entity_position=self.get_component(Entity,Position)
        distance=abs(nearest_entity_position.x-entity_position.x)+abs(nearest_entity_position.y-entity_position.y)
        # logger.info(f"Distance between entity {entity} and {Entity} is {distance}")
        if distance<nearest_distance:
          nearest_distance=distance
          nearest_entity=Entity
    logger.info(f"Nearest entity is {nearest_entity}")
    return nearest_entity

  def get_entity_at(self, x, y):
    return self.position_to_entity.get((x, y), [])
  
      






if  __name__=="__main__":
  world=World()
  world.add_component(1,Position(10,29))
  # # for _ in range(10):
  # #   entity=world.create_entity()
  print(world.remove_component(1,Position))
  