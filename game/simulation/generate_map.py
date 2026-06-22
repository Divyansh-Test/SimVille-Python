import random
import numpy as np
from logger_config import get_logger
logger=get_logger(__name__)
from world.creature import system


#layer0=Floor layer1=the thing in floor layer2=the entity on the layer

def generate_map(width, height, seed=None):
    
    np.random.seed(seed)
    layer_0=np.zeros((width, height), dtype=np.int8) # for tile layer
    #This is the fixed layer later will be replaced by procedural generation.
    layer_1=np.zeros((width, height), dtype=np.int8)
    
    rng = np.random.default_rng()

    idx = rng.choice(width * height, size=25, replace=False)
    pos = np.column_stack((idx % width, idx // width))
    for i in range(14):
        layer_1[pos[i][0],pos[i][1]]=system.create_entity(info={"name":"","type":"tree"},position=(pos[i][0],pos[i][1]),health=10,inventory={"wood":10,"stone":10},state="idle")
    for i in range(14,25):
        layer_1[pos[i][0],pos[i][1]]=system.create_entity(info={"name":"","type":"stone"},position=(pos[i][0],pos[i][1]),health=10,inventory={"wood":10,"stone":10},state="idle")

    

    
        
        
     # for object layer
    layer_2=np.full((width, height),-1, dtype=np.int16) # for entity layer

    return layer_0,layer_1,layer_2







