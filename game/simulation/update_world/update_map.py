from world.Map import WorldMap
from world.creature import components
from logger_config import get_logger
logger=get_logger(__name__)
logger.error("Reached here")
Map=WorldMap(10,10,seed=42)
layer0,layer1,layer2=Map.layer0,Map.layer1,Map.layer2
def get_layer():
   global layer0,layer1,layer2
   return layer0,layer1,layer2

def update_map():
   global layer2
   
   for  id in components["position"]:
      x,y=components["position"][id]
      layer2[y][x]=id
      
   return  layer2
      
   