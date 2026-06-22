from world.Map import WorldMap
from world.creature import components
import copy
from logger_config import get_logger
logger=get_logger(__name__)
height=10
width=10
Map=WorldMap(height,width,seed=42)
layer0,layer1,layer2=Map.layer0,Map.layer1,Map.layer2
layer1_orig=copy.deepcopy(layer1)
#logger.info(f"layer2_orig{layer2_orig}")
def get_layer():
   global layer0,layer1,layer2
   return layer0,layer1,layer2

def update_map():
    # restore original layer2
    layer1[:][:] =layer1_orig[:][:]
    # for y, row in enumerate(layer2_orig):
    #     layer2[y][:] = row[:]
    for creature_id, (x, y) in components["position"].items():
        layer1[y][x] = creature_id

    return layer2