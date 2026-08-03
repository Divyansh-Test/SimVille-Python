from ecs.components.inventory import Inventory
from ecs.components.position import Position # Import your position component
import random
from logger_config import get_logger

logger = get_logger(__name__)

def get_empty_coordinate(world):
    target_x = random.randint(0, world.height-1)
    target_y = random.randint(0, world.width-1)
    
    # Explicitly check is not None to avoid ID 0 bugs
    while world.get_entity_at(target_x, target_y) :
        target_x = random.randint(0, world.height-1)
        target_y = random.randint(0, world.width-1)
        
    return (target_x, target_y)

def get_empty_coordinate_near(entity, world, radius=2):
    pos = world.get_component(entity, Position)
    
    if pos is None:
        return get_empty_coordinate(world)
        
    start_x, start_y = pos.x, pos.y
    
    for _ in range(10):
        target_x = max(0, min(14, start_x + random.randint(-radius, radius)))
        target_y = max(0, min(14, start_y + random.randint(-radius, radius)))
        
        # Explicit check prevents placing over entity ID 0
        if world.get_entity_at(target_x, target_y) is None:
            return (target_x, target_y)
            
    return get_empty_coordinate(world)


def try_build_house(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if inventory is None: return None

    site_id = world.find_nearest_entity(entity, "Construction Site")
    
    # If no site exists, check if we even need a house before placing a blueprint
    if site_id is None:
        existing_house = world.find_nearest_entity(entity, "House")
        if existing_house is not None:
            return None # We already have a house. Skip to next rule.
            
        target_coord = get_empty_coordinate_near(entity, world)
        logger.info(f"Entity {entity} queuing PlaceBlueprint for House at {target_coord}.")
        return [{"type": "PlaceBlueprint", "blueprint": "House", "target": target_coord, "priority": 85}]

    NEEDED_WOOD = 5
    NEEDED_STONE = 5
    wood_amount = inventory.items.get("Wood", 0)
    stone_amount = inventory.items.get("Stone", 0)

    # Gather missing resources
    if wood_amount < NEEDED_WOOD:
        wood_source = world.find_nearest_entity(entity, "Wood")
        if wood_source is not None:
            return [{"type": "Gather", "target": wood_source, "priority": 80}]
        return [{"type": "Explore", "target": get_empty_coordinate(world), "priority": 80}]

    if stone_amount < NEEDED_STONE:
        stone_source = world.find_nearest_entity(entity, "Stone")
        if stone_source is not None:
            return [{"type": "Gather", "target": stone_source, "priority": 80}]
        return [{"type": "Explore", "target": get_empty_coordinate(world), "priority": 80}]

    logger.info(f"Entity {entity} has all materials. Queuing Transfer and Build jobs for Site {site_id}.")
    return [
        {"type": "Build", "target": site_id, "priority": 85},
        {"type": "Transfer", "target": site_id, "action": "put", "item": "Wood", "amount": NEEDED_WOOD, "priority": 90},
        {"type": "Transfer", "target": site_id, "action": "put", "item": "Stone", "amount": NEEDED_STONE, "priority": 90}
    ]

def try_plant_crops(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if inventory is None: return None

    farm_plot = world.find_nearest_entity(entity, "FarmPlot")
    
    if farm_plot is None:
        # Check if we are already building the FarmPlot as a Construction Site
        site_id = world.find_nearest_entity(entity, "Construction Site")
        if site_id is not None:
            return None # Let try_build_house finish building it first
            
        target_coord = get_empty_coordinate_near(entity, world)
        logger.info(f"Entity {entity} queuing PlaceBlueprint for FarmPlot at {target_coord}.")
        return [{"type": "PlaceBlueprint", "blueprint": "FarmPlot", "target": target_coord, "priority": 85}]

    seed_amount = inventory.items.get("Seed", 0)
    
    if seed_amount < 1:
        seed_source = world.find_nearest_entity(entity, "Seed")
        if seed_source is not None:
            return [{"type": "Gather", "target": seed_source, "priority": 80}]
        return [{"type": "Explore", "target": get_empty_coordinate(world), "priority": 80}]

    return [
        {"type": "Plant", "target": farm_plot, "priority": 35},
        {"type": "Transfer", "target": farm_plot, "action": "put", "item": "Seed", "amount": 1, "priority": 40}
    ]

def try_transfer_excess(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if inventory is None: return None

    wood_count = inventory.items.get("Wood", 0)
    if wood_count > 10:
        chest_id = world.find_nearest_entity(entity, "Chest") 
        if chest_id is not None:
            return [
                {"type": "Transfer", "target": chest_id, "action": "put", "item": "Wood", "amount": wood_count - 5, "priority": 60}
            ]
        return [{"type": "Explore", "target": get_empty_coordinate(world), "priority": 60}]
    return None

def try_explore(entity, world, spawner):
    return [
        {"type": "Explore", "target": get_empty_coordinate(world), "priority": 10}
    ]


# FIXED: The order of rules is now strictly aligned with your priority comments
work_rules = [
#    try_build_house,      # Highest Priority: Finish any active construction sites
#    try_plant_crops,      # Second Priority: Secure renewable food source
#    try_transfer_excess,  # Third Priority: Clean up inventory
    try_explore           # Absolute Last: Only run if literally nothing else is possible
]
