from simulation.update_world.update_time import update_time
from simulation.update_world.update_entity import update_creature
from simulation.update_world.update_map import update_map,layer2
from logger_config import get_logger
logger=get_logger(__name__)
def update_all():
   
   update_creature()
   c=update_time()
   m=update_map()
   logger.info(f"layer2{layer2}")