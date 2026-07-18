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
            "Shore":self.spawn_shore_resources
        }

    def is_tile_available(self, x, y, terrain_id=0):
        width = len(self.terrain_layer)
        if width == 0:
            return False
        height = len(self.terrain_layer[0])

        if not (0 <= x < width and 0 <= y < height):
            return False

        if self.terrain_layer[x][y] != terrain_id:
            return False

        for entity in self.world.get_entity_with(Position):
            p = self.world.get_component(entity, Position)
            if p.x == x and p.y == y:
                return False

        return True

    def get_valid_spawn_tile(self, position=None, terrain_id=0, fallback_search=None):
        if position is not None:
            if self.is_tile_available(position[0], position[1], terrain_id):
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

        occupied = set()
        for entity in self.world.get_entity_with(Position):
            p = self.world.get_component(entity, Position)
            occupied.add((p.x, p.y))

        for _ in range(100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if self.terrain_layer[x][y] == 0: 
                if (x, y) not in occupied:
                    return (x, y)
        return None

    def find_water_tile(self, pos=None):
        width = len(self.terrain_layer)
        if width == 0:
            return None
        height = len(self.terrain_layer[0])

        occupied = set()
        for entity in self.world.get_entity_with(Position):
            p = self.world.get_component(entity, Position)
            occupied.add((p.x, p.y))

        for _ in range(100):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            if self.terrain_layer[x][y] == 1:
                if (x, y) not in occupied:
                    return (x, y)
        return None

    def find_tile_near_water(self, pos=None):
        width = len(self.terrain_layer)
        if width == 0:
            return None
        height = len(self.terrain_layer[0])

        occupied = set()
        for entity in self.world.get_entity_with(Position):
            p = self.world.get_component(entity, Position)
            occupied.add((p.x, p.y))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in range(50):
            water_pos = self.find_water_tile()
            if not water_pos:
                return None

            wx, wy = water_pos

            for dx, dy in directions:
                nx, ny = wx + dx, wy + dy

                if 0 <= nx < width and 0 <= ny < height:
                    if self.terrain_layer[nx][ny] == 0:
                        if (nx, ny) not in occupied:
                            return (nx, ny)

        return None

    def spawn_tree(self, position=None):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            data = ENTITIES["Tree"]
            health = random.randint(*data["Health"])
            death_age = random.randint(*data["death_age"])
            interval = data["interval"]
            inventory = {}
            for item, value in data["Inventory"].items():
                inventory[item] = random.randint(*value)

            tree_entity = self.world.create_entity()
            self.world.add_component(tree_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Tree"), Renderable("♣"), Growth(interval, death_age))
            return tree_entity

    def spawn_stone(self, position=None):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            data = ENTITIES["Stone"]
            health = random.randint(*data["Health"])
            inventory = {}
            for item, value in data["Inventory"].items():
                inventory[item] = random.randint(*value)

            stone_entity = self.world.create_entity()
            self.world.add_component(stone_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Stone"), Renderable("◆"))
            return stone_entity

    def spawn_npc(self, position=None):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            data = ENTITIES["Human"]
            health = random.randint(*data["Health"])
            hunger = random.randint(*data["Hunger"])
            death_age = random.randint(*data["death_age"])
            interval = data["interval"]
            inventory = {}
            for item, value in data["Inventory"].items():
                inventory[item] = random.randint(*value)

            npc_entity = self.world.create_entity()
            self.world.add_component(npc_entity, Position(tile[0], tile[1]), Health(health),
                                      State("Idle"), Inventory(inventory),
                                      Type("Human"), Hunger(hunger), Renderable("♂"), Growth(interval, death_age))
            return npc_entity

    def spawn_house(self, position=None):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            data = ENTITIES["House"]
            health = data["Health"]

            house_entity = self.world.create_entity()
            self.world.add_component(house_entity, Position(tile[0], tile[1]), Health(health),
                                      State("idle"), Type("House"), Renderable("H"))
            return house_entity

    def spawn_chest(self, position=None):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            chest_entity = self.world.create_entity()
            self.world.add_component(chest_entity, Position(tile[0], tile[1]), Inventory({}), State("idle"), Type("Chest"), Renderable("⌂"))
            return chest_entity

    def spawn_construction_site(self, position=None, **kwargs):
        tile = self.get_valid_spawn_tile(position)
        if tile:
            logger.info(f"tile is {tile}")
            construction_site_entity = self.world.create_entity()
            self.world.add_component(construction_site_entity, Position(tile[0], tile[1]), State("idle"), Type("Construction Site"), Renderable("?"), Inventory({}), Blueprint(kwargs["blueprint"]))
            return construction_site_entity

    def spawn_shore_resources(self, position=None,**kwargs):
        tile=self.get_valid_spawn_tile(position,fallback_search=self.find_tile_near_water)
        if tile:
            logger.info(f"tile is for water_shore {tile}")
            shore_entity=self.world.create_entity()
            data=ENTITIES["ShoreResource"]
            health=random.randint(*data["Health"])
            inventory={}
            for item,value in data["Inventory"].items():
                inventory[item]=random.randint(*value)
            self.world.add_component(shore_entity,Position(tile[0],tile[1]),Health(health),State("idle"),Type("ShoreResource"),Renderable("*"),Inventory(inventory))
        return shore_entity 

    def spawn_entity(self, type, position=None, **kwargs):
        if type in self.spawn_registry:
            return self.spawn_registry[type](position, **kwargs)