class GameTime:
  def  __init__(self):
    self.hour=0
    self.day=1
    self.month=1
    self.year=0
    self.min=1
    self.month_list=[]

  def update_time(self):
    self.min+=1
    if self.min>50:
       self.min=0
       self.hour+=1
    if self.hour>23:
       self.hour=0
       self.day+=1
    if  self.day>30:
       self.day=0
       self.month+=1

    if self.month>=12:
       self.month=0
       self.year+=1







if  __name__=="__main__":
  a=GameTime()
  for _ in range(1000001):
     a.update_time()
  print(f"Min is {a.min} Hour is {a.hour} Day is {a.day} Month is {a.month} Year is {a.year}")