from ecs.components.position import Position
from ecs.components.move_to import MoveTo
from ecs.components.path import Path
from logger_config import get_logger
logger=get_logger(__name__)


class MovementSystem:
    def __init__(self, world):
        self.world = world

    def update(self):
        for entity in self.world.get_entity_with(Position,MoveTo):
            # logger.info(f"Entity {entity} is moving and has a path {self.world.get_component(entity,Path).path}")
            next=self.world.get_component(entity,Path).path.pop()
            self.world.get_component(entity,Position).x=next[0]
            self.world.get_component(entity,Position).y=next[1]
            
