import random
from ecs.components.position import Position
from ecs.components.health import Health
from ecs.components.state import State
from ecs.components.job import Job
from ecs.components.inventory import Inventory
from ecs.components.type import Type
from ecs.components.renderable import Renderable
from ecs.components.hunger import Hunger
from ecs.components.blueprint import Blueprint
from ecs.components.growth import Growth
from ecs.components.vision import Vision
from data.entities import ENTITIES
from logger_config import get_logger

logger = get_logger(__name__)

class Spawner:
    def __init__(self, world, terrain_layer):
        self.world = world
        self.terrain_layer = terrain_layer
        self.spawn_registry = {
            "Tree": self.spawn_tree,
            "Stone": self.spawn_stone,
            "NPC": self.spawn_npc,
            "House": self.spawn_house,
            "Chest": self.spawn_chest,
            "ConstructionSite": self.spawn_construction_site,
            "Shore": self.spawn_shore_resources,
            "FarmPlot": self.spawn_farm_plot,
            "Plant": self.spawn_plant,
            "Seedling": self.spawn_seedling,
        }

    def _generate_inventory(self, data_dict):
        """Helper to generate a randomized inventory dict from ENTITIES data."""
        inventory = {}
        for item, value in data_dict.get("Inventory", {}).items():
            inventory[item] = random.randint(*value)
        return inventory

    def _get_entity_type_string(self, entity):
        """Safely extracts the type string from a Type component."""
        if self.world.has_component(entity, Type):
            type_comp = self.world.get_component(entity, Type)
            
            return type_comp.type
        return None

    def is_tile_available(self, x, y, terrain_id=0, ignore_entity=None, valid_parents=None):
        logger.info(f"Checking tile {x}, {y} for terrain {terrain_id} and valid_parent are {valid_parents}")
        width = len(self.terrain_layer)
        if width == 0:
            return False
        height = len(self.terrain_layer[0])

        if not (0 <= x < width and 0 <= y < height):
            return False

        if self.terrain_layer[x][y] != terrain_id:
            return False

        # O(1) Instant spatial map check
        
        occupants = self.world.position_to_entity.get((x, y), []).copy()
        
        # Start by assuming all entities on the tile (except the builder) are blocking
        blocking_entities = [ent for ent in occupants if ent != ignore_entity]
        logger.info(f'occupants are {occupants} and ignoring the entity {ignore_entity}')

        if valid_parents:
            parent_found = False
            for ent in occupants:
                ent_type = self._get_entity_type_string(ent)
                if ent_type in valid_parents:
                    parent_found = True
                    logger.info("parent entity is {ent}")
                    # The parent is expected to be here, so it does not count as a block
                    if ent in blocking_entities:
                        blocking_entities.remove(ent)
                    break # We only need one valid parent

            if not parent_found:
                logger.info(f"Tile {x}, {y} rejected: Missing required parent from {valid_parents}")
                return False

        if blocking_entities:
            logger.info(f"Tile {x}, {y} is blocked by entities {blocking_entities}")
            return False

        logger.info(f"Tile {x}, {y} is available")
        return True

    def get_valid_spawn_tile(self, position=None, terrain_id=0, fallback_search=None, ignore_entity=None, valid_parents=None):
        if position is not None:
            if self.is_tile_available(position[0], position[1], terrain_id, ignore_entity, valid_parents):
                return position
            else:
                logger.warning(f"Spawn aborted: Position {position} is occupied or invalid.")
                return None

        if fallback_search:
            return fallback_search()

        return self.find_grass_tile()

    def find_grass_tile(self, pos=None):
        width = len(self.terrain_layer)
        if width == 0:
            return None
        height = len(self.terrain_layer[0])

        for _ in range(100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if self.terrain_layer[x][y] == 0 and (x, y) not in self.world.position_to_entity:
                return (x, y)
        return None

    def find_water_tile(self, pos=None):
        width = len(self.terrain_layer)
        if width == 0:
            return None
        height = len(self.terrain_layer[0])

        for _ in range(100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if self.terrain_layer[x][y] == 1 and (x, y) not in self.world.position_to_entity:
                return (x, y)
        return None

    def find_tile_near_water(self, pos=None):
        width = len(self.terrain_layer)
        if width == 0:
            return None
        height = len(self.terrain_layer[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in range(50):
            water_pos = self.find_water_tile()
            if not water_pos:
                return None

            wx, wy = water_pos

            for dx, dy in directions:
                nx, ny = wx + dx, wy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if self.terrain_layer[nx][ny] == 0 and (nx, ny) not in self.world.position_to_entity:
                        return (nx, ny)
        return None

    # ------------- SPAWNERS ------------- #

    def spawn_tree(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["Tree"]
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            health = random.randint(*data["Health"])
            death_age = random.randint(*data["death_age"])
            inventory = self._generate_inventory(data)

            tree_entity = self.world.create_entity()
            self.world.add_component(tree_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Tree"), Renderable("tree.png",data["size"][0],data["size"][1]), Growth(data["interval"], death_age))
            return tree_entity

    def spawn_stone(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["Stone"]
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            health = random.randint(*data["Health"])
            inventory = self._generate_inventory(data)

            stone_entity = self.world.create_entity()
            self.world.add_component(stone_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Stone"), Renderable("stone.png"))
            return stone_entity

    def spawn_npc(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["Human"]
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            health = random.randint(*data["Health"])
            hunger = random.randint(*data["Hunger"])
            death_age = random.randint(*data["death_age"])
            inventory = self._generate_inventory(data)

            npc_entity = self.world.create_entity()
            self.world.add_component(npc_entity, Position(tile[0], tile[1]), Health(health),
                                      State("Idle"), Vision(2), Inventory(inventory),
                                      Type("Human"), Hunger(hunger), Renderable("npc.png",data["size"][0],data["size"][1]), Growth(data["interval"], death_age))
            return npc_entity

    def spawn_house(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["House"]
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            house_entity = self.world.create_entity()
            self.world.add_component(house_entity, Position(tile[0], tile[1]), Health(data["Health"]),
                                      State("idle"), Type("House"), Renderable("H"))
            return house_entity

    def spawn_chest(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES.get("Chest", {})
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            chest_entity = self.world.create_entity()
            self.world.add_component(chest_entity, Position(tile[0], tile[1]), Inventory({"Wood":20}), State("idle"), Type("Chest"), Renderable("chest.png"))
            return chest_entity

    def spawn_farm_plot(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES.get("FarmPlot", {})
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            farm_entity = self.world.create_entity()
            self.world.add_component(farm_entity, Position(tile[0], tile[1]), State("idle"),Inventory({}), Type("FarmPlot"), Renderable("farm_land.png"))
            return farm_entity

    def spawn_seedling(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["Seedling"]
        # Seedling MUST have valid_parents=["Farm Plot"]
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            seedling_entity = self.world.create_entity()
            death_age = random.randint(*data["death_age"])
            self.world.add_component(seedling_entity, Position(tile[0], tile[1]), State("idle"), Type("Seedling"),  Renderable("seedling.png"), Growth(data["interval"], death_age))
            return seedling_entity

    def spawn_plant(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES.get("Plant", {})
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            plant_entity = self.world.create_entity()
            death_age = random.randint(*data["death_age"])
            self.world.add_component(plant_entity, Position(tile[0], tile[1]), State("idle"), Type("Plant"), Renderable("plant.png"),Growth(data["interval"], death_age))
            return plant_entity

    def spawn_construction_site(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES.get("Construction Site", {})
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            construction_site_entity = self.world.create_entity()
            self.world.add_component(construction_site_entity, Position(tile[0], tile[1]), State("idle"), Type("ConstructionSite"), Renderable("error.png"), Inventory({}), Blueprint(kwargs.get("blueprint")))
            return construction_site_entity

    def spawn_shore_resources(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        data = ENTITIES["ShoreResource"]
        tile = self.get_valid_spawn_tile(position, fallback_search=self.find_tile_near_water, ignore_entity=builder, valid_parents=data.get("spawn_parent"))
        if tile:
            health = random.randint(*data["Health"])
            inventory = self._generate_inventory(data)

            shore_entity = self.world.create_entity()
            self.world.add_component(shore_entity, Position(tile[0], tile[1]), Health(health), State("idle"), Type("ShoreResource"), Renderable("shore.png"), Inventory(inventory))
            return shore_entity 

    def spawn_entity(self, type, position=None, **kwargs):
        if type in self.spawn_registry:
            return self.spawn_registry[type](position, **kwargs)
