class Job:
  def  __init__(self,job=None):
     self.job=[job]

  def update(self,other):
     self.job.extend(other)