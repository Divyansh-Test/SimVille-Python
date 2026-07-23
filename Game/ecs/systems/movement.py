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
            pos=self.world.get_component(entity,Position)
            prev_pos=(pos.x,pos.y)
            pos.x,pos.y=next
            self.world.position_to_entity[prev_pos].remove(entity)
            key = (pos.x, pos.y)
            self.world.position_to_entity.setdefault(key, []).append(entity)
            
            
            
            
