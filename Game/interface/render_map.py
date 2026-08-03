# interface/render_map.py
import pygame
from ecs.components.position import Position
from ecs.components.renderable import Renderable
from ecs.components.state import State
from ecs.components.move_to import MoveTo

# Safe imports for Overlays (Prevents crashes if these components aren't fully built yet)
try:
    from ecs.components.vision import Vision
except ImportError:
    Vision = None

try:
    from ecs.components.job import Job
except ImportError:
    Job = None

try:
    from ecs.components.path import Path
except ImportError:
    Path = None

TERRAIN_ASSETS = {
    1: "water.png",
    0: "grass.png",
    2: "farm_land.png",
    3: "shore.png"
}

def render_map(world, terrain_layer, map_surface, assets, tile_size, camera, state):
    draw_list = []
    font_small = pygame.font.SysFont(None, 18)

    # =============================================================
    # 1. Collect Environment Terrain
    # =============================================================
    for row in range(len(terrain_layer)):
        for col in range(len(terrain_layer[row])):
            screen_x = (col * tile_size) - camera.x
            screen_y = (row * tile_size) - camera.y
            
            # Frustum Culling Check
            if screen_x < -tile_size or screen_x > camera.width or screen_y < -tile_size or screen_y > camera.height:
                continue

            terrain_val = terrain_layer[row][col]
            image_name = TERRAIN_ASSETS.get(terrain_val, "error.png")
            surface = assets.get_image(image_name, tile_size, tile_size)
            
            draw_list.append({
                "surface": surface,
                "x": screen_x,
                "y": screen_y,
                "sort_y": screen_y 
            })

    # =============================================================
    # 2. Collect Entities for Y-Sorting
    # =============================================================
    for entity in world.get_entity_with(Position, Renderable):
        position = world.get_component(entity, Position)
        render_comp = world.get_component(entity, Renderable)
        
        target_width = render_comp.width_tiles * tile_size
        target_height = render_comp.height_tiles * tile_size
        
        screen_x = (position.y * tile_size) - camera.x
        screen_y = (position.x * tile_size) - camera.y - (target_height - tile_size)

        if screen_x < -target_width or screen_x > camera.width or screen_y < -target_height or screen_y > camera.height:
            continue
            
        image_name = render_comp.image_file 
        surface = assets.get_image(image_name, target_width, target_height)
        
        # Y-Sort Anchor (Bottom of the sprite)
        sort_y_axis = screen_y + target_height

        draw_list.append({
            "surface": surface,
            "x": screen_x,
            "y": screen_y,
            "sort_y": sort_y_axis
        })

    # =============================================================
    # 3. Blit Base Graphics (Y-Sorted)
    # =============================================================
    draw_list.sort(key=lambda item: item["sort_y"])
    for item in draw_list:
        map_surface.blit(item["surface"], (item["x"], item["y"]))

    # =============================================================
    # 4. F1-F4 DEBUG OVERLAYS (Drawn strictly on top of sprites)
    # =============================================================
    # Only loop through entities again if at least one overlay is turned on
    if state["show_vision"] or state["show_path"] or state["show_target"] or state["show_jobs"]:
        
        for entity in world.get_entity_with(Position):
            pos = world.get_component(entity, Position)
            
            # Center of the entity in screen coordinates
            center_x = (pos.y * tile_size) - camera.x + (tile_size // 2)
            center_y = (pos.x * tile_size) - camera.y + (tile_size // 2)

            # Culling check for overlays
            if center_x < -100 or center_x > camera.width + 100 or center_y < -100 or center_y > camera.height + 100:
                continue

            # F1: Vision Radius (Translucent Circle)
            if state["show_vision"] and Vision and world.has_component(entity, Vision):
                vision_comp = world.get_component(entity, Vision)
                radius_tiles = getattr(vision_comp, 'radius', 5) # Default to 5 tiles if no attribute
                radius_pixels = radius_tiles * tile_size
                pygame.draw.circle(map_surface, (255, 255, 100), (center_x, center_y), radius_pixels, 1)

            # F2: Path Visualization (Drawing lines across nodes)
            if state["show_path"] and Path and world.has_component(entity, Path):
                path_comp = world.get_component(entity, Path)
                route = getattr(path_comp, 'path', []) # Expects list of (row, col) tuples
                
                if route and len(route) > 0:
                    points = [(center_x, center_y)]
                    for (r, c) in route:
                        px = (c * tile_size) - camera.x + (tile_size // 2)
                        py = (r * tile_size) - camera.y + (tile_size // 2)
                        points.append((px, py))
                    
                    if len(points) > 1:
                        pygame.draw.lines(map_surface, (100, 150, 255), False, points, 2)

            # F3: Target Line (Direct line to goal)
            if state["show_target"] and MoveTo and world.has_component(entity, MoveTo):
                job_comp = world.get_component(entity, MoveTo)
                target_x = getattr(job_comp, 'x', None) # Expects (row, col) tuple
                target_y = getattr(job_comp, 'y', None) # Expects (row, col) tuple
                target=(target_x,target_y)
                
                if target:
                    target_x = (target[1] * tile_size) - camera.x + (tile_size // 2)
                    target_y = (target[0] * tile_size) - camera.y + (tile_size // 2)
                    pygame.draw.line(map_surface, (255, 100, 100), (center_x, center_y), (target_x, target_y), 2)
                    pygame.draw.circle(map_surface, (255, 100, 100), (target_x, target_y), 4)

            # F4: Job Pop-ups (Floating Text)
            if state["show_jobs"] and State and world.has_component(entity, State):
                job_comp = world.get_component(entity, State)
                job_name = getattr(job_comp, 'state', 'Idle')
                
                
                # Create a small dark background block for readable text
                text_surf = font_small.render(job_name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(midbottom=(center_x, center_y - (tile_size // 2) - 5))
                
                bg_rect = text_rect.inflate(8, 4)
                pygame.draw.rect(map_surface, (30, 30, 30), bg_rect, border_radius=3)
                pygame.draw.rect(map_surface, (100, 100, 100), bg_rect, 1, border_radius=3)
                
                map_surface.blit(text_surf, text_rect)
