import random
import numpy as np


#layer0=Floor layer1=the thing in floor layer2=the entity on the layer

def generate_map(width, height, seed=None):
    items=[0,1,2]
    prob_item=[0.5,0.3,0.2]
    np.random.seed(seed)
    layer_0=np.zeros((width, height), dtype=np.int8) # for tile layer
    layer_1=np.random.choice(items,size=(width, height),p=prob_item) # for object layer
    layer_2=np.full((width, height),-1, dtype=np.int16) # for entity layer

    return layer_0,layer_1,layer_2







