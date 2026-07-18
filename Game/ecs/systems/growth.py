from ecs.components.growth import Growth
from ecs.components.position import Position
from ecs.components.type import Type
from logger_config import get_logger
from data.entities import ENTITIES
import random
logger=get_logger(__name__)
class GrowthSystem():
   def __init__(self,world,spawner):
      self.world=world
      self.spawner=spawner
      self.respawn_queue=[]

   def update(self):
      for entity in  self.world.get_entity_with(Growth):
         growth=self.world.get_component(entity,Growth)
         age=growth.age
         # logger.info(f"Entity {entity} has age {age}")
         death_age=growth.death_age
         if age>=death_age:
            logger.info(f"Entity {entity} has died at age {age}")
            # position=self.world.get_component(entity,Position)
            # x_rand=random.randint(-1,1)
            # y_rand=random.randint(-1,1)
            # position=(position.x+x_rand,position.y+y_rand)
            type=self.world.get_component(entity,Type).type
            self.add_respawn(type,(self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y))
            self.world.destroy_entity(entity)
            # Spawn the tree trunk or similiar effect here
            #spawner.spawn("trunk",position)
            continue
         next_upd= growth.next_update
         if self.world.tick>=next_upd:
            growth.update()
      for respawn in self.respawn_queue:
         if self.world.tick>=respawn["respawn_time"]:
            logger.info(f"Entity {respawn['type']} is respawning at {respawn['pos']}")
            self.spawner.spawn_entity(respawn["type"],respawn["pos"])
            self.respawn_queue.remove(respawn)
   
   
   
   def add_respawn(self,type,pos):
      respawn_interval=random.randint(*ENTITIES[type]["respawn_interval"])
      self.respawn_queue.append({
         "type":type,
         "pos":pos,
         "respawn_time":self.world.tick+respawn_interval
      })
      logger.info(f"Entity {type} will respawn at {pos} in {respawn_interval} ticks and tick is {self.world.tick+respawn_interval}")
      