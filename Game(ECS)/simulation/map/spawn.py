from  ecs.components.position import Position
from  ecs.components.health import Health
from  ecs.components.state import State
from  ecs.components.job import Job
from  ecs.components.inventory import Inventory
from  ecs.components.type import Type 
from  ecs.components.renderable import Renderable
from ecs.world  import  World
import random
def find_grass_tile(world,terrain_layer):
   
   
   while True:
      
      x = random.randint(0, 14)
      y = random.randint(0, 14)

                          # Not walkable
      if terrain_layer[y][x] != 0:
         
         continue

                          # Check if an entity is already there
      occupied = False
      for entity in world.get_entity_with(Position):
         pos = world.get_component(entity, Position)
         if pos.x == x and pos.y == y:
            
            
            occupied = True
            break

      if not occupied:
         return (y,x)

      



def spawn_animal(world,terrain_layer):
   grass_tile=find_grass_tile(world,terrain_layer)
   if grass_tile:
      animal_entity=world.create_entity()
      world.add_component(animal_entity,Position(grass_tile[0],grass_tile[1]),Health(100),State("idle"),Type("animal"),Renderable("▼"))
      return animal_entity


def spawn_tree(world,terrain_layer):
   grass_tile=find_grass_tile(world,terrain_layer)
   if grass_tile:
      tree_entity=world.create_entity()
      world.add_component(tree_entity,Position(grass_tile[0],grass_tile[1]),Health(100),State("idle"),Type("tree"),Renderable("♣"))
      return tree_entity




def spawn_stone(world,terrain_layer):
   grass_tile=find_grass_tile(world,terrain_layer)
   if grass_tile:
      stone_entity=world.create_entity()
      world.add_component(stone_entity,Position(grass_tile[0],grass_tile[1]),Health(100),State("idle"),Type("stone"),Renderable("◆"))
      return stone_entity


def spawn_npc(world,terrain_layer):
   grass_tile=find_grass_tile(world,terrain_layer)
   if grass_tile:
      npc_entity=world.create_entity()
      world.add_component(npc_entity,Position(grass_tile[0],grass_tile[1]),Health(100),State("idle"),Inventory({"wood":10,"stone":10}),Type("Human"),Renderable("♂"))
      return npc_entity
      
