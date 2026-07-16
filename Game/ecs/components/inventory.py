class Inventory:
  def __init__(self, items=None):
      self.items = {} if items is None else items

  def update(self, items):
      for  item,amount in items.items():
         self.items[item]=amount

      for  key in list(self.items.keys()):
           amount=self.items[key]
           if amount<=0:
                self.items.pop(key)