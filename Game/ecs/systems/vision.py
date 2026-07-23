from ecs.components.vision import Vision
from ecs.components.position import Position
from logger_config import get_logger
logger=get_logger(__name__)
class  VisionSystem:
   def __init__(self,world):
      self.world=world

   def update(self):
        for entity in self.world.get_entity_with(Vision):
          vision = self.world.get_component(entity, Vision)
          pos = self.world.get_component(entity, Position)

          visible = set()

          x_min = max(0, pos.x - vision.range)
          x_max = min(self.world.width, pos.x + vision.range + 1)

          y_min = max(0, pos.y - vision.range)
          y_max = min(self.world.height, pos.y + vision.range + 1)

          for x in range(x_min, x_max):
              for y in range(y_min, y_max):
                  entities = self.world.get_entity_at(x, y)
                  

                  if not entities:
                      continue

                  for other in entities:
                      if other != entity:
                          visible.add(other)

          vision.update(list(visible))
              