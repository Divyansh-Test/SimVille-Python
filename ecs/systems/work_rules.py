from ecs.components.inventory import Inventory
from logger_config import get_logger

logger = get_logger(__name__)

def try_build_house(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if not inventory:
        return None

    # Define exact requirements
    NEEDED_WOOD = 5
    NEEDED_STONE = 5

    wood_amount = inventory.items.get("Wood", 0)
    stone_amount = inventory.items.get("Stone", 0)

    # 1. Prerequisite Check: Gather Wood if short
    if wood_amount < NEEDED_WOOD:
        wood_source = world.find_nearest_entity(entity, "Wood")
        logger.info(f"Wood source is {wood_source}")
        if wood_source:
            logger.debug(f"Entity {entity} needs {NEEDED_WOOD - wood_amount} more Wood to build.")
            return [{"type": "Gather", "target": wood_source}]
        return None # Cannot find wood, job fails for now

    # 2. Prerequisite Check: Gather Stone if short
    if stone_amount < NEEDED_STONE:
        stone_source = world.find_nearest_entity(entity, "Stone")
        logger.info(f"Stone source is {stone_source}")
        if stone_source:
            logger.debug(f"Entity {entity} needs {NEEDED_STONE - stone_amount} more Stone to build.")
            return [{"type": "Gather", "target": stone_source}]
        return None # Cannot find stone, job fails for now

    # 3. All prerequisites met. Execute Building Phase.
    site_id = world.find_nearest_entity(entity, "Construction Site")

    if not site_id:
        logger.info(f"Entity {entity} is laying down a new Construction Site blueprint.")
        site_id = spawner.spawn_entity("Construction Site", blueprint="House")
        if not site_id:
            logger.error("Spawner failed to return a valid ID for Construction Site.")
            return None

    # Push the final execution stack
    return [
        {"type": "Build", "target": site_id},
        {"type": "Transfer", "target": site_id, "action": "put", "item": "Wood", "amount": NEEDED_WOOD},
        {"type": "Transfer", "target": site_id, "action": "put", "item": "Stone", "amount": NEEDED_STONE},
    ]

def try_craft_stone_axe(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if not inventory:
        return None

    # If they already have an axe, skip crafting
    if inventory.items.get("StoneAxe", 0) > 0:
        return None

    NEEDED_WOOD = 1
    NEEDED_STONE = 1

    wood_amount = inventory.items.get("Wood", 0)
    stone_amount = inventory.items.get("Stone", 0)

    # Check prerequisites dynamically
    if wood_amount < NEEDED_WOOD:
        wood_source = world.find_nearest_entity(entity, "Wood")
        if wood_source:
            return [{"type": "Gather", "target": wood_source}]
        return None

    if stone_amount < NEEDED_STONE:
        stone_source = world.find_nearest_entity(entity, "Stone")
        if stone_source:
            return [{"type": "Gather", "target": stone_source}]
        return None

    # All prerequisites met. Execute craft.
    return [{"type": "Craft", "target": None, "item": "StoneAxe", "amount": 1}]

def try_transfer_excess(entity, world, spawner):
    inventory = world.get_component(entity, Inventory)
    if not inventory:
        return None

    # Dumping excess materials into the hardcoded chest
    wood_count = inventory.items.get("Wood", 0)
    if wood_count > 10:
        chest_id = 51 
        return [
            {"type": "Transfer", "target": chest_id, "action": "put", "item": "Wood", "amount": wood_count - 5}
        ]
    return None

work_rules= [
    try_build_house,
    try_craft_stone_axe,
    try_transfer_excess
]