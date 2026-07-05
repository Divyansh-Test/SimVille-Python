from world.creature import components,system
from simulation.update_world.update_map import layer0
from logger_config import get_logger
logger=get_logger(__name__)  

c1=system.create_entity(info={"name":"Vaibhav","type":"human"},position=(0,0),health=100,inventory={"wood":10,"stone":10},state="idle")
components["jobs"]={c1:{"type":"Gather","target":201}}





def update_creature():
  pass
  # logger.info(f"components dict is \n{components['jobs']}\n")
  
   