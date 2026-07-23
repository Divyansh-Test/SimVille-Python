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
from ecs.systems.growth import GrowthSystem
from logger_config import get_logger
import  curses
import time
world=World()
map=Map(15,15)
movement=MovementSystem(world)
spawn=Spawner(world,map.terrain_layer)
growth=GrowthSystem(world,spawn)
job=JobSystem(world,map,spawn,growth)
ai=AISystem(world,map,spawn)
hunger=HungerSystem(world)

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
   spawn.spawn_entity("Tree")

for _ in range(20):
   spawn.spawn_entity("Stone")
for _ in range(1):
   spawn.spawn_entity("Chest")
for _ in range(1):
   spawn.spawn_entity("NPC")

for _ in range(21):
    spawn.spawn_entity("Shore")




ai.pseudo_update()





while True:
    world.tick+=1
    
    #ai.update()
    growth.update()

    hunger.update()
    job.update()
    movement.update()
    render_system.update()
    time.sleep(0.2)
    