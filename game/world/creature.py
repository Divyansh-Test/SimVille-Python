creature_id=100
def get_creature():
     global  creature_id
     creature_id+=1
     return creature_id


components={"entity":{},
"health":{},
"hunger":{},
"position":{},
"inventory":{},
"state":{}


}
class system:
    def movement_system(id):
        pass
    
    def create_entity(**kwarg):
        id=get_creature()
        for key,value in kwarg.items():
            components[key][id]=value
        components["entity"]=id
        return id
        
       
        
       
    def add_state(id,state):
        components["state"][id]=state
    
    
    
    
    def get_component(id,name):
       return components[name].get(id)
       
    
    
    
    def get_item(id,item):
      items=get_component(id,"inventory")
      if item not in items:
         return 0
    
      else:
         return items.get(item)
    
    
    def update_item(id,item,amount):
        items = get_component(id, "inventory")
    
        new_amount = items.get(item, 0) + amount
    
        if new_amount <= 0:
            if item in items:
                del items[item]
        else:
            items[item] = new_amount
    
        return True
    
    
    
    
    
    def update_health(id,amount):
       health=get_component(id,"health")
       health+=amount
       components["health"][id]=health
       if health<=0:
          destroy_entity(id)
    
       else:
          
          return True
    
    
    def destroy_entity(id):
       for comp in components.values():
           if id in  comp:
              del comp[id]