from ecs.components.inventory import Inventory
from ecs.components.hunger import Hunger
import random
from logger_config import get_logger

logger = get_logger(__name__)

def get_empty_coordinate(world):
    # Map is 15x15, so valid indices are 0 to 14
    target_x = random.randint(0, 14)
    target_y = random.randint(0, 14)
    
    # Keep rolling until get_entity_at returns nothing (None or empty list)
    while world.get_entity_at(target_x, target_y):
        target_x = random.randint(0, 14)
        target_y = random.randint(0, 14)
        
    return (target_x, target_y)

def try_eat(entity, world, spawner):
    hunger_comp = world.get_component(entity, Hunger)
    if not hunger_comp or hunger_comp.hunger > 70:
        return None

    inventory = world.get_component(entity, Inventory)
    if inventory and inventory.items.get("Food", 0) > 0:
        return [{"type": "Consume", "item": "Food", "target": None, "priority": 100}]
        
    return None

def try_gather_food(entity, world, spawner):
    hunger_comp = world.get_component(entity, Hunger)
    if not hunger_comp or hunger_comp.hunger > 40:
        return None

    target = world.find_nearest_entity(entity, "Food") 
    
    if not target:
        target_coord = get_empty_coordinate(world)
        logger.debug(f"Entity {entity} is hungry but sees no food. Exploring to {target_coord}.")
        return [{"type": "Explore", "target": target_coord, "priority": 95}]
     
    return [
        {"type": "Consume", "item": "Food", "target": None, "priority": 100},
        {"type": "Gather", "target": target, "priority": 95}
    ]
    
hunger_rules = [
    try_eat,
    try_gather_food,
]
