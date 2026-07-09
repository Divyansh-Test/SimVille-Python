
from ecs.world import World
from ecs.components.position import Position
from ecs.components.health import Health
from ecs.components.hunger import Hunger
from ecs.components.job import Job
from ecs.components.inventory import Inventory
from ecs.components.state import State
from ecs.systems.movement import MovementSystem

def test():
   world=World()
   movement=MovementSystem(world)
   entity = world.create_entity()
   entity2 = world.create_entity()
   entity3 = world.create_entity()
   entity4 = world.create_entity()
   entity5 = world.create_entity()
   entity6 = world.create_entity()
   entity7 = world.create_entity()
   entity8 = world.create_entity()
   entity9 = world.create_entity()
   entity10 = world.create_entity()
   entity11 = world.create_entity()
   entity12 = world.create_entity()
   entity13 = world.create_entity()
   entity14 = world.create_entity()
   entity15 = world.create_entity()

   # Player
   world.add_component(
       entity,
       Position(10, 29),
       Health(100),
       Hunger(100),
       Job("farmer"),
       Inventory(),
       State("idle")
   )

   # Tree
   world.add_component(
       entity2,
       Position(15, 20),
       Health(50),
       Job("tree"),
       State("standing")
   )

   # Stone
   world.add_component(
       entity3,
       Position(8, 12),
       Health(200),
       Job("stone"),
       State("idle")
   )

   # Cow
   world.add_component(
       entity4,
       Position(18, 17),
       Health(80),
       Hunger(70),
       Job("cow"),
       State("wandering")
   )

   # Wheat
   world.add_component(
       entity5,
       Position(12, 22),
       Health(20),
       Job("wheat"),
       State("growing")
   )

   # Berry Bush
   world.add_component(
       entity6,
       Position(20, 8),
       Health(35),
       Job("bush"),
       State("fruiting")
   )

   # Wolf
   world.add_component(
       entity7,
       Position(25, 16),
       Health(120),
       Hunger(90),
       Job("wolf"),
       State("hunting")
   )

   # House
   world.add_component(
       entity8,
       Position(30, 30),
       Health(300),
       Inventory(),
       Job("house"),
       State("built")
   )

   # Chest
   world.add_component(
       entity9,
       Position(28, 26),
       Health(40),
       Inventory(),
       Job("chest"),
       State("closed")
   )

   # Merchant
   world.add_component(
       entity10,
       Position(35, 15),
       Health(100),
       Hunger(80),
       Inventory(),
       Job("merchant"),
       State("trading")
   )

   # Sheep
   world.add_component(
       entity11,
       Position(14, 9),
       Health(70),
       Hunger(60),
       Job("sheep"),
       State("grazing")
   )

   # Iron Rock
   world.add_component(
       entity12,
       Position(42, 6),
       Health(250),
       Job("iron"),
       State("idle")
   )

   # Campfire
   world.add_component(
       entity13,
       Position(16, 27),
       Health(30),
       Job("campfire"),
       State("burning")
   )

   # Water
   world.add_component(
       entity14,
       Position(5, 5),
       Job("water"),
       State("still")
   )

   # Villager
   world.add_component(
       entity15,
       Position(9, 18),
       Health(100),
       Hunger(95),
       Inventory(),
       Job("villager"),
       State("walking")
   )

   # Test get_component
   print(world.get_component(entity, Position).x)  # Expected: 10
   print(world.get_component(entity2, Health).health)  # Expected: 50
   print(world.get_entity_with(Position))
   print(world.get_entity_with(Position,Health))
   print(world.get_entity_with(Position,Health,Hunger))
   print(world.get_entity_with(Position,Health,Hunger,Job))
   movement.update()
   print(world.get_component(entity,Position).x)
   
  
   




if __name__=="__main__":
   test()
  