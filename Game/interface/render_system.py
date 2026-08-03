# interface/render_system.py
import pygame
import os
from interface.render_map import render_map
from interface.render_ui import render_ui
from config import VIEWPORT_WIDTH, TOP_UI_HEIGHT

class AssetManager:
    def __init__(self):
        self.cache = {}

    def get_image(self, filename, target_width, target_height):
        cache_key = f"{filename}_{target_width}x{target_height}"
        if cache_key not in self.cache:
            path = os.path.join("assets", filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.cache[cache_key] = pygame.transform.scale(img, (target_width, target_height))
            except FileNotFoundError:
                surf = pygame.Surface((target_width, target_height))
                surf.fill((255, 0, 255)) 
                self.cache[cache_key] = surf
        return self.cache[cache_key]


class RenderSystem:
    def __init__(self, world, terrain_layer, screen, map_surface, tile_size, camera):
        self.world = world
        self.terrain_layer = terrain_layer
        self.screen = screen
        self.map_surface = map_surface
        self.tile_size = tile_size
        self.camera = camera
        self.assets = AssetManager()
        self.ui_rects = {}

    def update(self, state):
        # 1. Clear Map Surface
        self.map_surface.fill((0, 0, 0))

        # 2. Draw Game Map & Entities inside Viewport
        # We now pass 'state' so the map renderer knows if it needs to draw F1-F4 overlays
        render_map(self.world, self.terrain_layer, self.map_surface, self.assets, self.tile_size, self.camera, state)
        
        # 3. Blit Map Surface onto Screen below Top UI Bar
        self.screen.blit(self.map_surface, (0, TOP_UI_HEIGHT))

        # 4. Render Top Bar & Sidebar UI (returns interactive rects)
        self.ui_rects = render_ui(self.screen, self.world, state, TOP_UI_HEIGHT)
