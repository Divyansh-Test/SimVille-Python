class Vision:
   def __init__(self,range,nearest_entities=[]):
      self.range=range
      self.nearest_entities=nearest_entities

   def update(self,entities,range=None):
      self.nearest_entities=entities
      if range:
         self.range=range