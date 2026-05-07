import numpy as np
import random
from database import tiles
ground_tiles=0
obj_tiles=1

def Map(size):
  np.random.seed(100)
  map=np.zeros((size,size,2),dtype=np.int32)
  tile_ids=[]
  tile_spawn_probablity=[]
  for tile_id,detail in tiles.items():
    
    tile_ids.append(tile_id)
    tile_spawn_probablity.append(detail["spawn_probablity"])

  tile_spawn_probablity=[x/sum(tile_spawn_probablity) for x in tile_spawn_probablity]

  occourance=np.random.choice(tile_ids,size=(10,10),p=tile_spawn_probablity)
  for i in range(10):
    for j in range(10):
      map[i,j,obj_tiles]=occourance[i,j]

  
  return map




def render():
  size=10
  map=Map(size)
  for i in range(size):
    for j in range(size):
      print(tiles[map[i,j,ground_tiles]]["symbol"],end=" ")
      print(tiles[map[i,j,obj_tiles]]["symbol"],end=" ")

    print(" \n \n ")
  
  
if __name__=="__main__":
  render()
  
