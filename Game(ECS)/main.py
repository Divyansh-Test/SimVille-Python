from  ecs.world import World
from ecs.systems.movement import MovementSystem
from simulation.map.map import Map
from simulation.map.spawn import spawn_tree,spawn_stone,spawn_npc

from interface.render_system import RenderSystem
from ecs.systems.job import JobSystem
from ecs.systems.ai import AISystem
from logger_config import get_logger
import  curses
import time
world=World()
map=Map(15,15)
movement=MovementSystem(world)
job=JobSystem(world,map)
ai=AISystem(world,map)
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
   spawn_tree(world,terrain_layer)

for _ in range(20):
   spawn_stone(world,terrain_layer)


for _ in range(5):
   spawn_npc(world,terrain_layer)
print(len(terrain_layer))




ai.update()
while True:
    

    movement.update()
    job.update()
    render_system.update()
    time.sleep(0.5)
  

