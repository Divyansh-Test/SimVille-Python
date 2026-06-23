from world.creature import components,system
from simulation.update_world.update_map import layer0
from logger_config import get_logger
logger=get_logger(__name__)  

c1=system.create_entity(info={"name":"Vaibhav","type":"human"},position=(0,0),health=100,inventory={"wood":10,"stone":10},state="idle")
c2=system.create_entity(info={"name":"Raj","type":"human"},position=(1,1),health=100,inventory={"wood":10,"stone":10},state="idle")
c3=system.create_entity(info={"name":"Raj","type":"human"},position=(2,2),health=100,inventory={"wood":10,"stone":10},state="idle")





def update_creature():
  system.movement_system(c1,[4,4],layer0)
  system.movement_system(c2,[4,4],layer0)
  system.movement_system(c3,[4,4],layer0)
  #logger.info(f"The position of the creature with id {c1} and name {components['info'][c1]['name']} is {components['position'][c1]}")
  
   