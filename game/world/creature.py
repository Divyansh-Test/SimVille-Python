import random
from ai.pathfinding import pathfinding
from logger_config import get_logger

logger=get_logger(__name__)
creature_id=100
tree_id=200
animal_id=300
stone_id=400

def get_creature(type):
     global  creature_id,tree_id,animal_id,stone_id
     if type=="tree":
         tree_id+=1
         return tree_id

     elif type=="animal":
         animal_id+=1
         return animal_id
     elif type=="stone":
         stone_id+=1
         return stone_id
     else:
         pass
         # logger.info("no type")
     creature_id+=1
     return creature_id


components={"info":{},
"entity":{},
"health":{},
"hunger":{},
"position":{},
"inventory":{},
"state":{},
"jobs":{},
"path":{}
}


class system:
    def movement_system(id,dest,layer0):
        path=components["path"].get(id)
        if not path and not (components["position"][id]==tuple(dest)):
            path=pathfinding(layer0,components["position"][id],dest)
            components["path"][id]=path
            
            logger.info(f"path called and path is {path}")
        
        if path:
            x,y=path.pop()
            components["position"][id]=(x,y)
        return True
        
    
    def create_entity(**kwarg):
        id=get_creature(kwarg["info"]["type"])
        for key,value in kwarg.items():
            components[key][id]=value
        #components["entity"][]=id
        return id
        
       
        
       
    def add_state(id,state):
        components["state"][id]=state
    
    
    
    
    def get_component(self,id,name):
       return components[name].get(id)
       
    
    
    
    def get_item(self,id,item):
      items=self.get_component(id,"inventory")
      if item not in items:
         return 0
    
      else:
         return items.get(item)
    
    
    
    
    
    
    def update_component(self, entity_id, component, amount=0, key=None):
        data = self.get_component(entity_id, component)
        
        if data is None:
            return False

        if key is None:
            # health, hunger, mana...
            data += amount
            components[component][entity_id] = data

            if component == "health" and data <= 0:
                self.destroy_entity(entity_id)
        
        
        else:
            # inventory or other nested dict components
            new_value = data.get(key, 0) + amount

            
            if new_value <= 0:
                data.pop(key, None)
            
            
            else:
                data[key] = new_value

        return True
    
    # def get_path(self,id,start,end,layer0):
    #     path=pathfinding(layer0,start,end)
    #     components["path"][id]=path
    #     logger.info(f"path called and path is {path}")
    #     return path
    
    
    def destroy_entity(id):
       for comp in components.values():
           
           
           if id in  comp:
              del comp[id]