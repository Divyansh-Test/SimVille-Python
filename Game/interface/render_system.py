import pygame
import os
from interface.render_map import render_map
from interface.render_ui import render_time, render_options

class AssetManager:
    def __init__(self):
        self.cache = {}

    def get_image(self, filename, tile_size):
        if filename not in self.cache:
            path = os.path.join("assets", filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.cache[filename] = pygame.transform.scale(img, (tile_size, tile_size))
            except FileNotFoundError:
                # Innovative fallback: Bright magenta signals a missing texture immediately
                surf = pygame.Surface((tile_size, tile_size))
                surf.fill((255, 0, 255)) 
                self.cache[filename] = surf
        return self.cache[filename]


class RenderSystem:
    def __init__(self, world, terrain_layer, screen, map_surface, ui_surface, tile_size):
        self.world = world
        self.terrain_layer = terrain_layer
        self.screen = screen
        self.map_surface = map_surface
        self.ui_surface = ui_surface
        self.tile_size = tile_size
        self.assets = AssetManager()

    def update(self):
        # 1. Clear previous frame
        self.map_surface.fill((0, 0, 0))
        self.ui_surface.fill((40, 40, 40)) 

        # 2. Render Map and Entities
        render_map(self.world, self.terrain_layer, self.map_surface, self.assets, self.tile_size)

        # 3. Render UI (Leave commented until we migrate them)
        # render_time(self.world, self.ui_surface)
        # render_options(self.world, self.ui_surface)

        # 4. Composite surfaces onto the main hardware screen
        self.screen.blit(self.map_surface, (0, 0))
        self.screen.blit(self.ui_surface, (self.map_surface.get_width(), 0))
