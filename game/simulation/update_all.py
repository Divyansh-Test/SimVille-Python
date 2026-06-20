from simulation.update_world.update_time import update_time
from simulation.update_world.update_entity import update_creature
from simulation.update_world.update_map import update_map
def update_all():
   print("Reached here")
   update_creature()
   c=update_time()
   # logger.info(f"layer2{c}")
   update_map()