from ecs.components.position import Position
from ecs.components.renderable import Renderable
from ecs.components.type import Type

# Map your old integer terrain IDs directly to your new PNG assets
TERRAIN_ASSETS = {
    1: "water.png",
    0: "grass.png",
}

def render_map(world, terrain_layer, map_surface, assets, tile_size):
    # 1. Render the Environment
    # We iterate by row (Y) and column (X) to map precisely to pixels
    for row in range(len(terrain_layer)):
        for col in range(len(terrain_layer[row])):
            terrain_val = terrain_layer[row][col]

            # Default to "error.png" if an unknown terrain integer appears
            image_name = TERRAIN_ASSETS.get(terrain_val, "error.png")
            surface = assets.get_image(image_name, tile_size)

            # Translate grid coordinates to pixel coordinates
            pixel_x = col * tile_size
            pixel_y = row * tile_size

            map_surface.blit(surface, (pixel_x, pixel_y))

    # 2. Render the Entities
    # We query for Position and Renderable, not Type. Type does not draw anything.
    for entity in world.get_entity_with(Position, Renderable):
        position = world.get_component(entity, Position)
        render_comp = world.get_component(entity, Renderable)
        
        image_name = render_comp.image_file 
        surface = assets.get_image(image_name, tile_size)
        
        # SWAPPED: position.y (column) becomes pixel_x, position.x (row) becomes pixel_y
        pixel_x = position.y * tile_size
        pixel_y = position.x * tile_size
        
        map_surface.blit(surface, (pixel_x, pixel_y))
