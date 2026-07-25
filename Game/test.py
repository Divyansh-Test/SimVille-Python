import pygame
import sys
from ecs.world import World
from ecs.systems.movement import MovementSystem
from simulation.map.map import Map
from simulation.map.spawn import Spawner
from ecs.components.state import State
from ecs.components.inventory import Inventory
from ecs.components.position import Position
from ecs.components.job import Job
from ecs.components.hunger import Hunger
from ecs.components.blueprint import Blueprint

from ecs.components.path import Path
from ecs.components.type import Type
from interface.render_system import RenderSystem
from ecs.systems.job import JobSystem
from ecs.systems.ai import AISystem
from ecs.systems.hunger import HungerSystem
from ecs.systems.growth import GrowthSystem
from ecs.systems.vision import VisionSystem
from logger_config import get_logger

# 1. Define Pygame Spatial Constants
TILE_SIZE = 40
MAP_WIDTH_TILES = 15
MAP_HEIGHT_TILES = 15
UI_WIDTH_PIXELS = 300

# Calculate exact pixel dimensions
WINDOW_WIDTH = (MAP_WIDTH_TILES * TILE_SIZE) + UI_WIDTH_PIXELS
WINDOW_HEIGHT = MAP_HEIGHT_TILES * TILE_SIZE

world = World(MAP_WIDTH_TILES, MAP_HEIGHT_TILES)
map = Map(MAP_WIDTH_TILES, MAP_HEIGHT_TILES)
movement = MovementSystem(world)
spawn = Spawner(world, map.terrain_layer)
growth = GrowthSystem(world, spawn)
vision = VisionSystem(world)
job = JobSystem(world, map, spawn, growth)
ai = AISystem(world, map, spawn)
hunger = HungerSystem(world)

logger = get_logger(__name__)

# 2. Modern Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("AI Simulation Village")
clock = pygame.time.Clock()

# Create distinct surfaces mirroring your old curses layout
map_surface = pygame.Surface((MAP_WIDTH_TILES * TILE_SIZE, WINDOW_HEIGHT))
ui_surface = pygame.Surface((UI_WIDTH_PIXELS, WINDOW_HEIGHT))

# Pass Pygame parameters to RenderSystem instead of curses windows
terrain_layer = map.terrain_layer
render_system = RenderSystem(world, terrain_layer, screen, map_surface, ui_surface, TILE_SIZE)

# Spawning Logic
for _ in range(30): spawn.spawn_entity("Tree")
for _ in range(20): spawn.spawn_entity("Stone")
for _ in range(1): spawn.spawn_entity("Chest")
for _ in range(1): spawn.spawn_entity("NPC")
for _ in range(21): spawn.spawn_entity("Shore")

ai.pseudo_update()

# 3. Modern Game Loop
running = True
while running:
    world.tick += 1

    # Event Pump: Prevents OS from flagging the window as unresponsive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic Updates
#    ai.update()
    growth.update()
    vision.update()
    hunger.update()
    job.update()
    movement.update()

    # Render Update
    render_system.update()

    # Hardware Display Flip and Pacing
    pygame.display.flip()
    clock.tick(5) # Locks game at 5 FPS, replacing time.sleep(0.2)
#    logger.info(f"path found is {world.get_component(52,Path).path}")

pygame.quit()
sys.exit()
