from  ecs.world import World
from ecs.systems.movement import MovementSystem
from simulation.map.map import Map
from simulation.map.spawn import Spawner
from ecs.components.state import State
from ecs.components.inventory import Inventory
from ecs.components.position import Position
from ecs.components.job import Job
from ecs.components.hunger import Hunger
from ecs.components.blueprint import Blueprint
from ecs.components.type import Type
from interface.render_system import RenderSystem
from ecs.systems.job import JobSystem
from ecs.systems.ai import AISystem
from ecs.systems.hunger import HungerSystem
# from logger_config import get_logger
import  curses
import time
world=World()
map=Map(15,15)
movement=MovementSystem(world)
spawn=Spawner(world,map.terrain_layer)
job=JobSystem(world,map,spawn)
ai=AISystem(world,map,spawn)
hunger=HungerSystem(world)
import logging
logging.basicConfig(
    filename="App.log",
    filemode="w",   # overwrite file on each run
    level=logging.INFO,
    format="%(asctime)s | %(filename)s | %(message)s"
)
logger=logging.getLogger(__name__)




terrain_layer=map.terrain_layer
stdscr=curses.initscr()
height, width = stdscr.getmaxyx()
map_width = int(width * 0.75)
ui_width = width - map_width
map_win = curses.newwin(height, map_width, 0, 0)
ui_win = curses.newwin(height, ui_width, 0, map_width)



render_system=RenderSystem(world,terrain_layer,map_win,ui_win)
for _ in range(30):
   spawn.spawn_entity("Tree")

for _ in range(20):
   spawn.spawn_entity("Stone")
for _ in range(1):
   spawn.spawn_entity("Chest")
for _ in range(1):
   spawn.spawn_entity("NPC")




logger.info(f"Entity 52 has job ")

for e in world.get_entity_with(Type):
    logger.info(f"Entity {e} has type {world.get_component(e,Type).type} ")
# ai.update()
# if world.has_component(52,Job):
#     logger.info(f"Entity 52 has job {world.get_component(52,Job).job}")
# if world.has_component(53,Job):
     # logger.info(f"Entity 53 has job {world.get_component(53,Job).job}")
while True:
    logger.info(f'position of entity 52 is {world.get_component(52,Position).x,world.get_component(52,Position).y}')
    ai.update()
    
    hunger.update()
    job.update()
    movement.update()
    # render_system.update()
    # time.sleep(0.4)
    logger.info(f"inventory of entity 52 is {world.get_component(52,Inventory).items}")
   
def Logs():
    target_id = 52

    try:
        logger.info(f"========== DIAGNOSTIC SNAPSHOT: ENTITY {target_id} ==========")

        # 1. State Component
        if world.has_component(target_id, Position):
            logger.info(f"  [Position] Currently is: {world.get_component(target_id, Position).x,world.get_component(target_id, Position).y}")
        else:
            logger.warning(f"  [Position] Component missing!")
        if world.has_component(target_id, State):
            logger.info(f"  [State] Currently in state: {world.get_component(target_id, State).state}")
        else:
            logger.warning(f"  [State] Component missing!")

        # 2. Hunger Component
        if world.has_component(target_id, Hunger):
            logger.info(f"  [Hunger] Value: {world.get_component(target_id, Hunger).hunger}")
        else:
            logger.warning(f"  [Hunger] Component missing!")

        # 3. Job Component (Now iterates through your list of dicts)
        if world.has_component(target_id, Job):
            job_comp = world.get_component(target_id, Job)

            # Safely extract the list. Assumes your class stores it in self.job
            job_list = getattr(job_comp, 'job', []) 

            if isinstance(job_list, list) and len(job_list) > 0:
                logger.info(f"  [Job Stack] {len(job_list)} tasks in queue:")
                for index, job_dict in enumerate(job_list):
                    if isinstance(job_dict, dict):
                        j_type = job_dict.get('type', 'Unknown')
                        j_target = job_dict.get('target')
                        j_item = job_dict.get('item')
                        j_action = job_dict.get('action')
                        logger.info(f"    [{index}] Type: {j_type} | Target: {j_target} | Item: {j_item} | Action: {j_action}")
                    else:
                        logger.warning(f"    [{index}] Invalid job format: {job_dict}")
            else:
                logger.info(f"  [Job Stack] Component exists but list is empty or malformed.")
        else:
            logger.info(f"  [Job] Idle (No active Job component attached)")

        # 4. Inventory Component
        if world.has_component(target_id, Inventory):
            inv_comp = world.get_component(target_id, Inventory)
            items_dict = getattr(inv_comp, 'items', {})
            logger.info(f"  [Inventory] Contents:")
            if items_dict:
                for item_name, count in items_dict.items():
                    logger.info(f"    - {item_name}: {count}")
            else:
                logger.info(f"    - (Empty)")
        else:
            logger.warning(f"  [Inventory] Component missing!")

        logger.info(f"====================================================")
    except Exception as e:
        logger.error(f"Failed to log state for Entity {target_id}: {str(e)}")
