class  Growth:
  def __init__(self,interval,death_age,next_update=0,age=0):
     self.interval=interval
     self.next_update=next_update
     self.death_age=death_age
     self.age=age

  def update(self):
     self.next_update=self.next_update+self.interval
     self.age+=1