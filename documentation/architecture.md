# Architecture Guide

## 1. Core Architectural Pattern

The project uses an Entity-Component-System (ECS) pattern.

### Entity
An entity is a numeric ID stored in the world. It represents a thing in the simulation such as a tree, NPC, stone, or house.

### Component
A component is a data container attached to an entity. Examples include:

- `Position`
- `Inventory`
- `Health`
- `Hunger`
- `Type`
- `Job`
- `Vision`
- `Growth`
- `State`

### System
A system operates on entities that have certain components. Examples include:

- `MovementSystem`
- `JobSystem`
- `HungerSystem`
- `GrowthSystem`
- `VisionSystem`
- `AISystem`

This pattern keeps logic modular and lets systems react to component state without embedding everything in one giant class.

---

## 2. World Model

The central world object is defined in `Game/ecs/world.py`.

It includes:

- `next_entity_id` for entity creation
- `tick` for simulation time
- `position_to_entity` for spatial indexing
- `components` dictionary for component storage

The world is responsible for:

- creating entities
- attaching components
- checking whether entities have specific components
- retrieving entities by component combinations
- removing entities and updating position tracking
- finding nearby entities and grid occupancy

### Important Considerations

The world stores component dictionaries keyed by entity ID. That means each entity can be thought of as a bag of components.

This structure is simple and effective for a prototype, but it also means the system has a few limitations:

- component updates are somewhat ad hoc
- some `update` methods mutate component content in place
- spatial indexing may require careful cleanup
- entity identity and map occupancy require consistent management

---

## 3. Simulation Lifecycle

The main lifecycle is roughly:

1. create `World`
2. generate a map
3. spawn entities
4. create systems
5. run the main loop
6. each tick update world state
7. render visible state

The project keeps time through `world.tick`, which is incremented in the game loop.

---

## 4. Map and Terrain

Map generation happens in:

- `Game/simulation/map/map.py`
- `Game/simulation/map/generator.py`

Terrain is represented as a grid, likely with values such as:

- 0 for grass
- 1 for water
- 2 for farm land
- 3 for shore

The terrain grid is passed to the spawner and pathfinding routines.

---

## 5. Spawning and Entity Creation

`Spawner` is defined in `Game/simulation/map/spawn.py`.

It contains a registry of entity types:

- `Tree`
- `Stone`
- `NPC`
- `House`
- `Chest`
- `ConstructionSite`
- `Shore`
- `FarmPlot`
- `Plant`
- `Seedling`

Each spawn method creates a proper component set for the entity and tries to place it in a valid tile.

Examples:

- trees have `Health`, `Inventory`, `Type`, `Renderable`, `Growth`
- NPCs have `Hunger`, `Vision`, `Inventory`, `State`, etc.
- farm plots and seedlings use parent validation and special spawn rules

This is a central mechanism for world population.

---

## 6. AI and Job Logic

The project uses a rule-based decision layer rather than a trained model.

### Main AI Layer

`AISystem` in `Game/ecs/systems/ai.py` evaluates entities with a hunger component and assigns jobs based on priority. It supports:

- survival rules before productivity rules
- rule evaluation order
- job stack assignment to an entity

### Job System

`JobSystem` in `Game/ecs/systems/job.py` executes the active job for each entity. It supports job types such as:

- `Gather`
- `Consume`
- `Transfer`
- `Craft`
- `Build`
- `Explore`
- `Plant`
- `PlaceBlueprint`

### Rule Files

The actual decision rules live in:

- `Game/ecs/systems/hunger_rules.py`
- `Game/ecs/systems/work_rules.py`

These rule functions decide what an NPC should do in response to hunger or world state.

---

## 7. Movement and Pathfinding

`MovementSystem` applies movement to entities that carry:

- `Position`
- `MoveTo`
- `Path`

`pathfinding.py` contains a simple A* style implementation using a grid and a heuristic.

### Notes

The pathfinding logic is intentionally lightweight and is not a production-grade navigation system. It works as a prototype for local movement and route planning in a tile grid.

---

## 8. Growth and Lifecycle

`GrowthSystem` in `Game/ecs/systems/growth.py` manages age-based entity lifecycle.

It:

- increases an entity’s age each tick
- checks if it reaches `death_age`
- destroys the entity if expired
- optionally spawns a successor or respawns a resource

This system is important for resource sustainability and lifecycle simulation.

---

## 9. Hunger and Resource Simulation

`HungerSystem` lowers hunger each tick for entities that have a `Hunger` component.

Rules in `hunger_rules.py` decide when an entity should:

- eat food
- gather food
- explore when necessary

This creates a simple survival loop that the simulation can run without explicit user commands.

---

## 10. Perception and Vision

`VisionSystem` and `PerceptionSystem` allow entities to understand nearby elements.

- `VisionSystem` gathers visible entities in a radius
- `PerceptionSystem` converts the detected entities into a perception dictionary

This is the main mechanism supporting environmental awareness for agents.

---

## 11. Rendering and User Interface

Rendering is handled under the `Game/interface` folder.

### Main rendering modules

- `render_system.py`: top-level render loop
- `render_map.py`: draws terrain and entity sprites
- `render_ui.py`: draws UI elements and controls
- `camera.py`: scroll and focus logic
- `curse_render.py`: terminal-based rendering concept

The active game entry point uses Pygame, while the project also has some terminal/curses-related code for alternate execution paths.

---

## 12. Data Definitions

The static entity and gameplay metadata live in:

- `Game/data/entities.py`
- `Game/data/items.py`
- `Game/data/recipes.py`
- `Game/data/blueprints.py`

These files define:

- entity health ranges
- resource inventories
- entity sizes
- crafting recipes
- building requirements
- respawn and lifecycle data

This layer makes the simulation easy to adjust without rewriting logic in systems.

---

## 13. Extending the Architecture

A common pattern for new features is:

1. define or reuse a component
2. attach the component in a spawner or world update
3. create or extend a system to react to it
4. add decision rules if it affects NPC behavior
5. add data definitions in `Game/data`

This pattern keeps the project maintainable as it grows.

---

## 14. Notable Architectural Risks

The following items are worth tracking as the project grows:

- some component classes may be too thin or inconsistent across the codebase
- job execution and state mutation can be fragile
- `Job` and `Inventory` behavior are not always normalized
- `World.update_component` has some non-trivial assumptions
- some spawn and world-tracking logic may not be fully robust under edge cases

These are normal issues for an early-stage ECS simulation and are good candidates for refactors.

---

## Conclusion

The architecture of SimVille-Python is intentionally simple, modular, and extensible. It provides a strong base for a world simulation, and the design cleanly separates data (components), behavior (systems), and world state (world manager).

The code is a practical prototype foundation for building a larger simulation or more advanced NPC systems in the future.
