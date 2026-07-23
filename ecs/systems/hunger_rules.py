from ecs.components.inventory import Inventory
from ecs.components.hunger import Hunger
from logger_config import get_logger

logger = get_logger(__name__)

def try_eat(entity, world, spawner):
    hunger_comp = world.get_component(entity, Hunger)
    if not hunger_comp:
        return None

    # Only care about eating if hunger has dropped below a safe threshold (e.g., 70)
    if hunger_comp.hunger > 70:
        return None

    inventory = world.get_component(entity, Inventory)
    if inventory and inventory.items.get("Food", 0) > 0:
        return [{"type": "Consume", "item": "Food", "target": None}]

    return None

def try_gather_food(entity, world, spawner):
    hunger_comp = world.get_component(entity, Hunger)
    if not hunger_comp:
        return None

    # CRITICAL FIX: If the entity is well-fed (hunger > 40), skip gathering food.
    # This allows the AI system to move to Productivity rules.
    if hunger_comp.hunger > 10:
        return None

    # Only search for food if actually hungry
    target = world.find_nearest_entity(entity, "Food") 
    if not target:
        return None

    return [
        {"type": "Gather", "target": target},
        {"type": "Consume", "item": "Food", "target": None}
    ]

hunger_rules = [
    try_eat,
    try_gather_food,
]