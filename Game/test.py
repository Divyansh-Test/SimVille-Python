# main.py
import pygame
import sys
from config import TILE_SIZE, MAP_WIDTH_TILES, MAP_HEIGHT_TILES, WINDOW_WIDTH, WINDOW_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, TOP_UI_HEIGHT

from ecs.world import World
from ecs.systems.movement import MovementSystem
from simulation.map.map import Map
from simulation.map.spawn import Spawner
from ecs.components.position import Position
from ecs.components.type import Type
from interface.render_system import RenderSystem
from interface.camera import Camera
from ecs.systems.job import JobSystem
from ecs.systems.ai import AISystem
from ecs.systems.hunger import HungerSystem
from ecs.systems.growth import GrowthSystem
from ecs.systems.vision import VisionSystem
from ecs.systems.perception import PerceptionSystem
from logger_config import get_logger

# ==========================================
# 1. INITIALIZATION & SETUP
# ==========================================
world = World(MAP_WIDTH_TILES, MAP_HEIGHT_TILES)
map = Map(MAP_WIDTH_TILES, MAP_HEIGHT_TILES)
perception=PerceptionSystem(world)
movement = MovementSystem(world)
spawn = Spawner(world, map.terrain_layer)
growth = GrowthSystem(world, spawn)
vision = VisionSystem(world)
job = JobSystem(world, map, spawn, growth)
ai = AISystem(world, map, spawn,perception)
hunger = HungerSystem(world)

logger = get_logger(__name__)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("AI Simulation Village")
clock = pygame.time.Clock()

map_surface = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

map_width_pixels = MAP_WIDTH_TILES * TILE_SIZE
map_height_pixels = MAP_HEIGHT_TILES * TILE_SIZE
camera = Camera(VIEWPORT_WIDTH, VIEWPORT_HEIGHT, map_width_pixels, map_height_pixels)

terrain_layer = map.terrain_layer
render_system = RenderSystem(world, terrain_layer, screen, map_surface, TILE_SIZE, camera)

# Spawning Entities
for _ in range(4): spawn.spawn_entity("NPC")
for _ in range(100): spawn.spawn_entity("Tree")
for _ in range(20): spawn.spawn_entity("Stone")
for _ in range(1): spawn.spawn_entity("Chest")
for _ in range(21): spawn.spawn_entity("Shore")

#ai.pseudo_update()

# ==========================================
# 2. RUNTIME STATE MANAGEMENT
# ==========================================
state = {
    "is_follow_mode": False,
    "selected_entity": None,
    "is_paused": False,
    "single_step": False,
    "sim_speed": 1,
    "running": True,
    # Overlays (F1 - F4)
    "show_vision": False,
    "show_path": False,
    "show_target": False,
    "show_jobs": False
}

camera_speed = TILE_SIZE

# ==========================================
# 3. MODULAR HELPER FUNCTIONS
# ==========================================
def handle_events(state, render_system, camera, world):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["running"] = False
            
        elif event.type == pygame.KEYDOWN:
            # Core Controls
            if event.key == pygame.K_SPACE:
                state["is_paused"] = not state["is_paused"]
            elif event.key == pygame.K_t and state["is_paused"]:
                state["single_step"] = True
            elif event.key == pygame.K_UP:
                state["sim_speed"] = min(5, state["sim_speed"] + 1)
            elif event.key == pygame.K_DOWN:
                state["sim_speed"] = max(1, state["sim_speed"] - 1)
                
            # F-Key Debug Overlays
            elif event.key == pygame.K_F1:
                state["show_vision"] = not state["show_vision"]
                #logger.info(f"Vision Overlay: {state['show_vision']}")
            elif event.key == pygame.K_F2:
                state["show_path"] = not state["show_path"]
                #logger.info(f"Path Overlay: {state['show_path']}")
            elif event.key == pygame.K_F3:
                state["show_target"] = not state["show_target"]
                #logger.info(f"Target Line Overlay: {state['show_target']}")
            elif event.key == pygame.K_F4:
                state["show_jobs"] = not state["show_jobs"]
                #logger.info(f"Job Popups: {state['show_jobs']}")
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            
            # A. UI Bar Clicks
            if my < TOP_UI_HEIGHT and mx < VIEWPORT_WIDTH:
                if render_system.ui_rects.get("follow_btn") and render_system.ui_rects["follow_btn"].collidepoint(mx, my):
                    state["is_follow_mode"] = not state["is_follow_mode"]
                    if state["is_follow_mode"]:
                        state["selected_entity"] = None
                elif render_system.ui_rects.get("pause_btn") and render_system.ui_rects["pause_btn"].collidepoint(mx, my):
                    state["is_paused"] = not state["is_paused"]
                elif render_system.ui_rects.get("speed_btn") and render_system.ui_rects["speed_btn"].collidepoint(mx, my):
                    speeds = [1, 2, 3, 5]
                    curr_idx = speeds.index(state["sim_speed"]) if state["sim_speed"] in speeds else 0
                    state["sim_speed"] = speeds[(curr_idx + 1) % len(speeds)]
                    
            # B. Viewport Map Clicks
            elif my >= TOP_UI_HEIGHT and my < (TOP_UI_HEIGHT + VIEWPORT_HEIGHT) and mx < VIEWPORT_WIDTH and state["is_follow_mode"]:
                world_x_pixels = mx + camera.x
                world_y_pixels = (my - TOP_UI_HEIGHT) + camera.y
                
                grid_col = world_x_pixels // TILE_SIZE
                grid_row = world_y_pixels // TILE_SIZE
                
                found_entity = None
                for entity in world.get_entity_with(Position):
                    pos = world.get_component(entity, Position)
                    if pos.x == grid_row and pos.y == grid_col:
                        found_entity = entity
                        break
                
                if found_entity is not None:
                    state["selected_entity"] = found_entity
                    state["is_follow_mode"] = False


def handle_camera(state, camera):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        state["selected_entity"] = None 
        if keys[pygame.K_w]: camera.move(0, -camera_speed)
        if keys[pygame.K_s]: camera.move(0, camera_speed)
        if keys[pygame.K_a]: camera.move(-camera_speed, 0)
        if keys[pygame.K_d]: camera.move(camera_speed, 0)

    if state["selected_entity"] is not None and world.has_component(state["selected_entity"], Position):
        pos = world.get_component(state["selected_entity"], Position)
        target_pixel_x = (pos.y * TILE_SIZE) + (TILE_SIZE // 2)
        target_pixel_y = (pos.x * TILE_SIZE) + (TILE_SIZE // 2)
        camera.update_target(target_pixel_x, target_pixel_y)

vision.update()
ai.pseudo_update()
def update_simulation_systems(state, world, growth, vision, hunger, job, movement):
    should_update = False
    iterations = 1

    if not state["is_paused"]:
        should_update = True
        iterations = state["sim_speed"]
    elif state["single_step"]:
        should_update = True
        iterations = 1
        state["single_step"] = False 

    if should_update:
        for _ in range(iterations):
            world.tick += 1
#            growth.update()
            vision.update()
            hunger.update()
            # ai.update()
            job.update()
            movement.update()


def handle_rendering(state, render_system):
    # Pass the entire state dictionary to the render system
    render_system.update(state)


# ==========================================
# 4. MAIN GAME LOOP EXECUTION
# ==========================================
while state["running"]:
    handle_events(state, render_system, camera, world)
    handle_camera(state, camera)
    update_simulation_systems(state, world, growth, vision, hunger, job, movement)
    handle_rendering(state, render_system)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
