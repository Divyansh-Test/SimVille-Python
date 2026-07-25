from utils.pathfinding import pathfinding
from ecs.components.position import Position
from ecs.components.job import Job
from ecs.components.path import Path
from ecs.components.move_to import MoveTo
from ecs.components.state import State
from ecs.components.type import Type
from ecs.components.health import Health
from ecs.components.inventory import Inventory
from ecs.components.hunger import Hunger
from ecs.components.blueprint import Blueprint
from ecs.component_registry import COMPONENTS
from data.items import ITEMS
from data.recipes import RECIPES
from data.blueprints import BLUEPRINTS
import time

from logger_config import get_logger
logger=get_logger(__name__)

class JobSystem:
   def __init__(self,world,map,spawnner,growthSystem):
      self.world=world
      self.map=map
      self.spawnner=spawnner
      self.growthSystem=growthSystem
      self.handlers={
         "Gather":self.Gather,
         "Consume":self.Consume,
         "Transfer":self.Tansfer,
         "Craft":self.Craft,
         "Build":self.Build,
         "Explore":self.Explore,
         "Plant":self.Plant,
         "PlaceBlueprint":self.PlaceBlueprint
      }

   def update(self):
     for entity in self.world.get_entity_with(Job):
        jobs=self.world.get_component(entity,Job).job
        if not jobs:
           self.world.remove_component(entity,Job)
           continue
     
        #this is the error bcuz we are accessing the last element of a empty list.
        highest_priority=0
        entity_job=None
        for job in jobs:
            if job["priority"]>highest_priority:
                highest_priority=job["priority"]
                entity_job=job
        logger.info(f"Entity {entity} has job {entity_job}")
        handler=self.handlers.get(entity_job["type"])
        if handler:
           handler(entity,entity_job)


   
   
   
   def get_path(self,entity,dest):
      # logger.info(f"Entity {entity} is moving to {dest}")
      if self.world.has_component(entity,Path):
         return
      start=(self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)

      self.world.add_component(entity,Path(pathfinding(start,dest,self.map.terrain_layer)))
      


   def  Gather(self,entity,job): # job dict = {"type":"Gather","target":entity_id,"item":item_name}
      


      

      # I think ki ye moveTo bekar hai Research karo
      target_id=job["target"]
      target=self.world.get_component(target_id,Position)
      target=(target.x,target.y)
      target_cord=self.move_job(entity,target)
      type=self.world.get_component(target_id,Type).type # instead we can take type from job as shore_res is the type but need water.
      self.world.add_component(entity,State(f"Gathering {type}")) 
      if  (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
          self.world.remove_component(entity,MoveTo)
          self.world.remove_component(entity,Path)
          health=self.world.get_component(target_id,Health).health-10
          self.world.update_component(target_id,Health(health))
          if self.world.get_component(target_id,Health).health<=0:
          
             self.world.get_component(entity,Job).job.remove(job)
             self.world.add_component(entity,State("idle"))
             target_inventory=self.world.get_component(target_id,Inventory).items
             entity_inventory=self.world.get_component(entity,Inventory).items
             for item in target_inventory.keys():
                 entity_inventory[item]=entity_inventory.get(item,0)+target_inventory[item]
             self.growthSystem.add_respawn(type,target_cord)
             self.world.destroy_entity(target_id)
             


   def move_job(self,entity,target):
      #This function will remove the line of code and also add path to the entity this will be only used by the jobs which needs to move somewhere.
      logger.info(f"target is {target}")
      
      
      # logger.info(f"target is {target}")
      self.get_path(entity,target)
      if not self.world.has_component(entity,MoveTo):
         self.world.add_component(entity,MoveTo(target[0],target[1]))
      return target

   def Consume(self, entity, job): # job dict = {"type":"Consume","target":None,"item":"food"}
      
       item = job["item"]
       effects = ITEMS[item]["consume"]

       inventory = self.world.get_component(entity, Inventory)
       if inventory.items.get(item, 0) <= 0 :
           logger.info(f"Entity {entity} does not have {item} to consume oor enough stats.")
           self.world.get_component(entity, Job).job.remove(job)
           self.world.add_component(entity, State("idle"))
           return
       self.world.update_component(entity, State(f"Consuming {item}"))
       all_full = True

       for effect, amount in effects.items():
           component_type, component_name, max_value = COMPONENTS[effect]

           current_value = getattr(
               self.world.get_component(entity, component_type),
               component_name
           )

           if current_value < max_value-15:
               all_full = False

           final_value = min(current_value + amount, max_value)

           self.world.update_component(entity, component_type(final_value))

       if all_full:
           x=self.world.get_component(entity, Job).job.remove(job)
           logger.info(f"Entity {entity} has finished consuming {item} and job is {x}")
           self.world.add_component(entity, State("idle"))
           return

       
       logger.info(f"Inventory of entity {entity} is {inventory.items}")
       stock=inventory.items.get(item, 0)-1
       stock=max(0,stock)
       # stock=inventory.items.get(item, 0)
       if stock >= 0:
         self.world.update_component(entity, Inventory({item: stock}))

   
   def Tansfer(self,entity,job): #job_dict={type:Tranfer,target=entity_id,action:put/take,item:item_name,amount:amount}
      item,amount=job["item"],job["amount"]
      target_id=job["target"]
      target=self.world.get_component(target_id,Position)
      target=(target.x,target.y)
      target_cord=self.move_job(entity,target)
      direction = "from" if job["action"] == "take" else "into"
      self.world.update_component(entity,State(f"{job['action']} {amount} {item} {direction} {job['target']}"))
      if (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
         self.world.remove_component(entity,MoveTo)
         self.world.remove_component(entity,Path)
         entity_stock=self.world.get_component(entity,Inventory).items.get(item,0)
         logger.info(f"target_ is is {target_id}")
         logger.info(f'target oitems are {self.world.get_component(target_id,Type).type}')
         target_stock=self.world.get_component(target_id,Inventory).items.get(item,0)
         
         if  job["action"]=="put":
             if entity_stock>=amount:
                self.world.update_component(entity,Inventory({item:entity_stock-amount}))
                self.world.update_component(job["target"],Inventory({item:target_stock+amount}))
             else:
                self.world.update_component(entity,Inventory({item:0}))
                self.world.update_component(job["target"],Inventory({item:target_stock+entity_stock}))
         elif  job["action"]=="take":
             logger.info(f"Entity {entity} is taking {amount} {item} from {job['target']} which ahs stock {target_stock}")
             if target_stock>=amount:
                 self.world.update_component(entity,Inventory({item:entity_stock+amount}))
                 self.world.update_component(job["target"],Inventory({item:target_stock-amount}))
             else:
                 self.world.update_component(entity,Inventory({item:entity_stock+target_stock}))
                 self.world.update_component(job["target"],Inventory({item:0}))
         
         self.world.get_component(entity,Job).job.remove(job)  
         self.world.update_component(entity,State("idle"))



   def Craft(self,entity,job): #job_dict={type:Craft,item:item_name,amount:amount}
      item,amount=job["item"],job["amount"]
      recipe=RECIPES[item]
      input_items=recipe["Input"]
      output_items=recipe["Output"]
      # Right now no checks here  for the input items and output items
      # we will add checks later
      self.world.update_component(entity,State(f"Crafting {amount} {item}"))
      for _ in range(amount):
         for input_item,input_amount in input_items.items():
             current_amount=self.world.get_component(entity,Inventory).items.get(input_item,0)
             logger.info(f'Right now the current amount of {input_item} is {current_amount}')
             self.world.update_component(entity,Inventory({input_item:current_amount-input_amount}))
         for output_item,output_amount in output_items.items():
             current_amount=self.world.get_component(entity,Inventory).items.get(output_item,0)
             self.world.update_component(entity,Inventory({output_item:current_amount+output_amount}))
      self.world.get_component(entity,Job).job.remove(job)
      self.world.update_component(entity,State("idle"))




   def Build(self,entity,job):
      target=job["target"]
      item=self.world.get_component(target,Blueprint).blueprint   
      
      item_req=BLUEPRINTS.get(item,{}).get("Input",0)
      available_item=self.world.get_component(target,Inventory).items
      
      logger.info(f'The item is {item} and  new dict is {available_item} and items needed are {item_req}')
      if all(available_item.get(k, 0) >= v for k, v in item_req.items()):
          
         
         logger.info(f"Entity {entity} has enough items to build")
         self.world.update_component(entity,State(f"Building {item}"))
         pos=self.world.get_component(target,Position)
         logger.info(f"Position of target is {pos.x,pos.y}")
         self.world.get_component(entity,Job).job.remove(job)
         self.spawnner.spawn_entity(item,(pos.x,pos.y),builder_entity=entity)
         self.world.destroy_entity(target)
         
         self.world.update_component(entity,State("idle"))



   def Explore(self,entity,job):
      target=job["target"]
      target_cord=self.move_job(entity,target)
      self.world.update_component(entity,State(f"Exploring the world"))
      if  (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
          self.world.remove_component(entity,MoveTo)
          self.world.remove_component(entity,Path)
          self.world.get_component(entity,Job).job.remove(job)
          self.world.update_component(entity,State("idle"))




   def Plant(self,entity,job):
      
      logger.info(f"1st line of plant")
      entity_inventory=self.world.get_component(entity,Inventory).items
      if entity_inventory.get("Seed",0)<=0:
         logger.info(f"entity dont has seed.")
         self.world.get_component(entity,Job).job.remove(job)
         self.world.update_component(entity,State("idle"))
         return
      logger.info(f"2st line of plant")
      target_id=job["target"]
      logger.info(f"3st line of plant")
      target=self.world.get_component(target_id,Position)
      logger.info(f"4st line of plant")
      target=(target.x,target.y)
      target_cord=self.move_job(entity,target)
      logger.info(f"target_cord is {target_cord}")
      target_inventory=self.world.get_component(target_id,Inventory).items
      logger.info(f"Reached here and target here in plant job and targetinventory is {target_inventory}")
      if  (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
          
          self.world.remove_component(entity,MoveTo)
          self.world.remove_component(entity,Path)
#          seed_available=entity_inventory.get("Seed",0)
#          self.world.update_component(target_id,Inventory({"Seed":1}))
#          self.world.update_component(entity,Inventory({"Seed":seed_available-1})) This is commented bcuz later i will add fertiliser etc to the farm.
          if target_inventory.get("Seed",0)<=0:
             self.world.get_component(entity,Job).job.remove(job)
             self.world.update_component(entity,State("idle"))
             return
          self.world.update_component(entity,State(f"Planting Seed"))
          self.spawnner.spawn_entity("Seedling",target_cord,builder_entity=entity)
          self.world.get_component(entity,Job).job.remove(job)



   def PlaceBlueprint(self,entity,job):
      logger.info(f"3st line of plant")
      
      target=job["target"]
      target_cord=self.move_job(entity,target)  
      if  (self.world.get_component(entity,Position).x,self.world.get_component(entity,Position).y)==target_cord:
          self.world.remove_component(entity,MoveTo)
          self.world.remove_component(entity,Path)
          id=self.spawnner.spawn_entity("ConstructionSite",position=target_cord,blueprint=job["blueprint"],builder_entity=entity)
          self.world.get_component(entity,Job).job.remove(job)
          logger.info(f"Spawned entity number {id}")
        
             
      
