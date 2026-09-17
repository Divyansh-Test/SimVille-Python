from ecs.components.vision import Vision
from ecs.components.position import Position
from ecs.components.type import Type
from logger_config import get_logger
logger = get_logger(__name__)


class PerceptionSystem:
    def __init__(self,world):
        self.world = world


    def decode(self, parent_entity):
        visible_entities = self.world.get_component(parent_entity, Vision).nearest_entities
         
        position = self.world.get_component(parent_entity, Position)
        perception={}
        for entity in visible_entities:
            entity_pos=self.world.get_component(entity, Position)
            distance = abs(position.x - entity_pos.x) + abs(position.y - entity_pos.y)
            type=self.world.get_component(entity, Type).type
            perception[entity]={
                "distance":distance,
                "type":type
            }

        logger.info(f"perception of {parent_entity}: {perception}")
        return perception




        