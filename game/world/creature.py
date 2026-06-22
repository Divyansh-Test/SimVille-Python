import random
from ai.pathfinding import pathfinding
from logger_config import get_logger
logger=get_logger(__name__)
creature_id=100
def get_creature():
     global  creature_id
     creature_id+=1
     return creature_id


components={"info":{},
"entity":{},
"health":{},
"hunger":{},
"position":{},
"inventory":{},
"state":{}


}
class system:
    def movement_system(id,dest,layer0):
        path=pathfinding(layer0,components["position"][id],dest)
        
        while path:
            x,y=path.pop()
            components["position"][id]=(x,y)
            return True
        
    
    def create_entity(**kwarg):
        id=get_creature()
        for key,value in kwarg.items():
            components[key][id]=value
        components["entity"]=id
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
    
    
    def update_item(self,id,item,amount):
        items = self.get_component(id, "inventory")
    
        new_amount = items.get(item, 0) + amount
    
        if new_amount <= 0:
            if item in items:
                del items[item]
        else:
            items[item] = new_amount
    
        return True
    
    
    
    
    
    def update_health(self,id,amount):
       health=self.get_component(id,"health")
       health+=amount
       components["health"][id]=health
       if health<=0:
          self.destroy_entity(id)
    
       else:
          
          return True
    
    
    def destroy_entity(self,id):
       for comp in components.values():
           if id in  comp:
              del comp[id]