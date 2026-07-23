from ecs.components.position import Position
from ecs.components.move_to import MoveTo
from ecs.components.path import Path
from logger_config import get_logger
logger=get_logger(__name__)


class MovementSystem:
    def __init__(self, world):
        self.world = world

    def update(self):
        # Always require Path component alongside MoveTo to prevent NoneType errors
        for entity in self.world.get_entity_with(Position, MoveTo, Path):
            path_comp = self.world.get_component(entity, Path)
            
            # 1. Safety Check: If path is empty, remove MoveTo and skip
            if not path_comp.path:
                self.world.remove_component(entity, MoveTo)
                continue
            
            # Get next coordinate. 
            # Note: pop() takes from the END of the list. 
            # Ensure your pathfinder returns lists as [destination, ..., next_step]
            next_pos = path_comp.path.pop() 
            
            pos = self.world.get_component(entity, Position)
            prev_pos = (pos.x, pos.y)
            
            # Update coordinate values
            pos.x, pos.y = next_pos
            
            # 2. Safe Spatial Map Removal and Cleanup
            if prev_pos in self.world.position_to_entity:
                logger.info(f"prev_pos is {prev_pos}")
                if entity in self.world.position_to_entity[prev_pos]:
                    self.world.position_to_entity[prev_pos].remove(entity)
                
                # Destroy the key entirely if the list is empty to save memory
                if not self.world.position_to_entity[prev_pos]:
                    del self.world.position_to_entity[prev_pos]
            
            # 3. Add to new position
            key = (pos.x, pos.y)
            self.world.position_to_entity.setdefault(key, []).append(entity)
            
            # 4. Final Cleanup: Did this step finish the journey?
            if not path_comp.path:
                self.world.remove_component(entity, MoveTo)
                # You might also want to trigger an "Arrived" event or state change here
            
            
            
            
