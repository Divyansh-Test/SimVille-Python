from world.creature import system,components
from simulation.update_world.update_map import layer0
from logger_config import get_logger
logger=get_logger(__name__)
''' job={1:{type:"Gather",target="tree ki id",}

}'''
class Jobsystem:
  def __init__(self):
    self.components=components


  def update(self):
    for id,jobs in  self.components["jobs"].items():
      target_id=self.reach(id)
      if self.components["jobs"][id]["type"]=="Gather":
        self.gather(id,target_id)



  def reach(self,id):
    target_id=self.components["jobs"][id]["target"]
    dest=self.components["position"][target_id]
    system.movement_system(id,dest,layer0)
    return target_id
    
    
  def gather(self,id,target_id):
    if self.components["position"][target_id]==self.components["position"][id]:
      # thsi is a temp logic to transfer all later this will be changed to transfer specific parts.
      self.components["inventory"][id]=self.components["inventory"][target_id]
      logger.info(f"inventory of {id} is {self.components['inventory'][id]}")
      system.destroy_entity(target_id)
      # del  self.components["jobs"][id]
    
    
    
      