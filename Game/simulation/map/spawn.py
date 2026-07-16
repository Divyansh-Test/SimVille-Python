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
from data.entities import ENTITIES
from logger_config import get_logger
logger=get_logger(__name__)


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
            "Construction Site":self.spawn_construction_site
        }

    def find_grass_tile(self):
        while True:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            if self.terrain_layer[y][x] != 0:
                continue
            occupied = False
            for entity in self.world.get_entity_with(Position):
                pos = self.world.get_component(entity, Position)
                if pos.x == x and pos.y == y:
                    occupied = True
                    break
            if not occupied:
                return (y, x)

    def spawn_tree(self, position=None):
        tile = position if position is not None else self.find_grass_tile()
        if tile:
            data = ENTITIES["Tree"]
            health = random.randint(*data["Health"])
            inventory = {}
            for item, value in data["Inventory"].items():
                inventory[item] = random.randint(*value)

            tree_entity = self.world.create_entity()
            self.world.add_component(tree_entity, Position(tile[0], tile[1]), Health(health),
                                      Inventory(inventory), State("idle"),
                                      Type("Tree"), Renderable("♣"))
            return tree_entity

    def spawn_stone(self, position=None):
        tile = position if position is not None else self.find_grass_tile()
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
        tile = position if position is not None else self.find_grass_tile()
        if tile:
            data = ENTITIES["Human"]
            health = random.randint(*data["Health"])
            hunger = random.randint(*data["Hunger"])
            inventory = {}
            for item, value in data["Inventory"].items():
                inventory[item] = random.randint(*value)

            npc_entity = self.world.create_entity()
            self.world.add_component(npc_entity, Position(tile[0], tile[1]), Health(health),
                                      State("Idle"), Inventory(inventory),
                                      Type("Human"), Hunger(hunger), Renderable("♂"))
            return npc_entity

    def spawn_house(self, position=None):
        tile = position if position is not None else self.find_grass_tile()
        if tile:
            data = ENTITIES["House"]
            health = data["Health"]

            house_entity = self.world.create_entity()
            self.world.add_component(house_entity, Position(tile[0], tile[1]), Health(health),
                                      State("idle"), Type("House"), Renderable("H"))
            return house_entity


    def spawn_chest(self, position=None):
        tile = position if position is not None else self.find_grass_tile()
        if tile:
            chest_entity = self.world.create_entity()
            self.world.add_component(chest_entity, Position(tile[0], tile[1]), Inventory({}), State("idle"),Type("Chest"), Renderable("⌂"))
            return chest_entity




    def spawn_construction_site(self, position=None,**kwargs):
        tile = position if position is not None else self.find_grass_tile()
        logger.info(f"tile is {tile}")
        if tile:
            construction_site_entity = self.world.create_entity()
            self.world.add_component(construction_site_entity, Position(tile[0], tile[1]), State("idle"), Type("Construction Site"), Renderable("?"),Inventory({}),Blueprint(kwargs["blueprint"]))
            return construction_site_entity

    def spawn_entity(self, type, position=None,**kwargs):
        if type in self.spawn_registry:
            return self.spawn_registry[type](position,**kwargs)