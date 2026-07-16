from  ecs.world import World
from ecs.systems.movement import MovementSystem
from simulation.map.map import Map
from simulation.map.spawn import Spawner
from ecs.components.state import State
from ecs.components.inventory import Inventory
from ecs.components.position import Position
from ecs.components.hunger import Hunger
from interface.render_system import RenderSystem
from ecs.systems.job import JobSystem
from ecs.systems.ai import AISystem
from ecs.systems.hunger import HungerSystem
from logger_config import get_logger
import  curses
import time
world=World()
map=Map(15,15)
movement=MovementSystem(world)
job=JobSystem(world,map)
ai=AISystem(world,map)
hunger=HungerSystem(world)
spawn_entity=Spawner(world,map.terrain_layer).spawn_entity
logger=get_logger(__name__)



terrain_layer=map.terrain_layer
stdscr=curses.initscr()
height, width = stdscr.getmaxyx()
map_width = int(width * 0.75)
ui_width = width - map_width
map_win = curses.newwin(height, map_width, 0, 0)
ui_win = curses.newwin(height, ui_width, 0, map_width)



render_system=RenderSystem(world,terrain_layer,map_win,ui_win)
for _ in range(30):
   spawn_entity("Tree")

for _ in range(20):
   spawn_entity("Stone")
for _ in range(1):
   spawn_entity("Chest")
for _ in range(2):
   spawn_entity("NPC")






ai.update()

while True:
    # ai.update()
    hunger.update()
    job.update()
    movement.update()
    render_system.update()
    time.sleep(0.3)
    
  

