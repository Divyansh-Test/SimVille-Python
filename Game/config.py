# config.py
TILE_SIZE = 32

# Map Dimensions (Easily scalable)
MAP_WIDTH_TILES = 40
MAP_HEIGHT_TILES = 40

# Window & UI Layout Dimensions
WINDOW_WIDTH =1500
WINDOW_HEIGHT = 900
UI_WIDTH_PIXELS = 550
TOP_UI_HEIGHT = 60 # Space reserved above the map for buttons

# Viewport math
VIEWPORT_WIDTH = WINDOW_WIDTH - UI_WIDTH_PIXELS
VIEWPORT_HEIGHT = WINDOW_HEIGHT - TOP_UI_HEIGHT
