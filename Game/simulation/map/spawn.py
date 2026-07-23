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
            "Construction Site": self.spawn_construction_site,
            "Shore": self.spawn_shore_resources,
            "Farm Plot": self.spawn_farm_plot,
            "Plant": self.spawn_plant,
            "Seedling": self.spawn_seedling,
        }

    def _generate_inventory(self, data_dict):
        """Helper to generate a randomized inventory dict from ENTITIES data."""
        inventory = {}
        for item, value in data_dict.get("Inventory", {}).items():
            inventory[item] = random.randint(*value)
        return inventory

    def is_tile_available(self, x, y, terrain_id=0, ignore_entity=None):
        logger.info(f"Checking tile {x}, {y} for terrain {terrain_id}")
        width = len(self.terrain_layer)
        if width == 0:
            return False
        height = len(self.terrain_layer[0])

        if not (0 <= x < width and 0 <= y < height):
            return False

        if self.terrain_layer[x][y] != terrain_id:
            return False

        # O(1) Instant spatial map check
        if (x, y) in self.world.position_to_entity:
            occupants = self.world.spatial_map[(x, y)]

            # Find any entity on this tile that is NOT the ignored entity
            blocking_entities = [ent for ent in occupants if ent != ignore_entity]

            if blocking_entities:
                logger.info(f"Tile {x}, {y} is occupied by entities {blocking_entities}")
                return False

        logger.info(f"Tile {x}, {y} is available")
        return True

    def get_valid_spawn_tile(self, position=None, terrain_id=0, fallback_search=None, ignore_entity=None):
        if position is not None:
            logger.info(f"Position is {position}")
            if self.is_tile_available(position[0], position[1], terrain_id, ignore_entity):
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

    def spawn_tree(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            data = ENTITIES["Tree"]
            health = random.randint(*data["Health"])
            death_age = random.randint(*data["death_age"])
            inventory = self._generate_inventory(data)

            tree_entity = self.world.create_entity()
            self.world.add_component(tree_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Tree"), Renderable("♣"), Growth(data["interval"], death_age))
            return tree_entity

    def spawn_stone(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            data = ENTITIES["Stone"]
            health = random.randint(*data["Health"])
            inventory = self._generate_inventory(data)

            stone_entity = self.world.create_entity()
            self.world.add_component(stone_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Stone"), Renderable("◆"))
            return stone_entity

    def spawn_npc(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            data = ENTITIES["Human"]
            health = random.randint(*data["Health"])
            hunger = random.randint(*data["Hunger"])
            death_age = random.randint(*data["death_age"])
            inventory = self._generate_inventory(data)

            npc_entity = self.world.create_entity()
            self.world.add_component(npc_entity, Position(tile[0], tile[1]), Health(health),
                                      State("Idle"), Vision(2), Inventory(inventory),
                                      Type("Human"), Hunger(hunger), Renderable("♂"), Growth(data["interval"], death_age))
            return npc_entity

    def spawn_house(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            data = ENTITIES["House"]
            house_entity = self.world.create_entity()
            self.world.add_component(house_entity, Position(tile[0], tile[1]), Health(data["Health"]),
                                      State("idle"), Type("House"), Renderable("H"))
            return house_entity

    def spawn_chest(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            chest_entity = self.world.create_entity()
            self.world.add_component(chest_entity, Position(tile[0], tile[1]), Inventory({"Wood":20}), State("idle"), Type("Chest"), Renderable("⌂"))
            return chest_entity

    def spawn_farm_plot(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        logger.info(f"tile is {tile} and position is {position} ")
        if tile:
            farm_entity = self.world.create_entity()
            self.world.add_component(farm_entity, Position(tile[0], tile[1]), State("idle"), Type("Farm"), Renderable("F"))
            return farm_entity

    def spawn_seedling(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            data = ENTITIES["Seedling"]
            seedling_entity = self.world.create_entity()
            death_age = random.randint(*data["death_age"])
            self.world.add_component(seedling_entity, Position(tile[0], tile[1]), State("idle"), Type("Plant"), Renderable("p"), Growth(data["interval"], death_age))
            return seedling_entity

    def spawn_plant(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            plant_entity = self.world.create_entity()
            self.world.add_component(plant_entity, Position(tile[0], tile[1]), State("idle"), Type("Plant"), Renderable("P"))
            return plant_entity

    def spawn_construction_site(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, ignore_entity=builder)
        if tile:
            logger.info(f"blueprint is {kwargs.get('blueprint')}")
            construction_site_entity = self.world.create_entity()
            self.world.add_component(construction_site_entity, Position(tile[0], tile[1]), State("idle"), Type("Construction Site"), Renderable("?"), Inventory({}), Blueprint(kwargs.get("blueprint")))
            return construction_site_entity

    def spawn_shore_resources(self, position=None, **kwargs):
        builder = kwargs.get("builder_entity")
        tile = self.get_valid_spawn_tile(position, fallback_search=self.find_tile_near_water, ignore_entity=builder)
        if tile:
            data = ENTITIES["ShoreResource"]
            health = random.randint(*data["Health"])
            inventory = self._generate_inventory(data)

            shore_entity = self.world.create_entity()
            self.world.add_component(shore_entity, Position(tile[0], tile[1]), Health(health), State("idle"), Type("ShoreResource"), Renderable("*"), Inventory(inventory))
            return shore_entity 

    def spawn_entity(self, type, position=None, **kwargs):
        if type in self.spawn_registry:
            return self.spawn_registry[type](position, **kwargs)