# API Reference

This document provides an API-style overview of the main classes and modules in SimVille-Python. It is intended for developers who want to understand the simulation interfaces, responsibilities, and extension points without reading every implementation file in full.

---

## 1. World API

### `World`
Location: `Game/ecs/world.py`

Purpose:
The central simulation registry. It owns entity lifecycle and component storage.

Signature:

```python
class World:
    def __init__(self, width, height):
        ...
```

Public methods:

```python
create_entity() -> int
```
Creates a new entity ID and returns it.

```python
add_component(entity, *components) -> None
```
Adds one or more component instances to an entity.

```python
update_component(entity, *components) -> None
```
Updates existing component data by type. This is the main mutation entry point for component changes.

```python
remove_component(entity, component_type) -> bool | None
```
Removes a component from an entity if present.

```python
get_component(entity, component_type)
```
Returns the component instance for an entity if it exists.

```python
has_component(entity, component_type) -> bool
```
Checks whether an entity has a component.

```python
get_entity_with(*component_types) -> set
```
Returns the set of entities that have all the given component types.

```python
destroy_entity(entity) -> None
```
Removes all components associated with an entity and cleans up spatial data.

```python
find_nearest_entity(entity, type_name)
```
Finds the closest nearby entity of the requested resource or entity type, using the current vision set and distance logic.

```python
get_entity_at(x, y) -> list
```
Returns the entities occupying a specific tile.

```python
entity_exists(entity) -> bool
```
Checks whether an entity still exists in the world.

Notes:
- `World.position_to_entity` is used as a spatial lookup map.
- `World.components` stores all component collections keyed by component type.
- `width` and `height` are used for world bounds and visibility calculations.

---

## 2. Map API

### `Map`
Location: `Game/simulation/map/map.py`

Purpose:
Wraps the generated terrain layer for the world.

Signature:

```python
class Map:
    def __init__(self, width, height):
        ...
```

Public fields:

```python
self.width
self.height
self.terrain_layer
```

Behavior:
- creates a tile grid from terrain generation logic
- exposes the terrain layer to spawners, movement systems, and rendering code

---

## 3. Spawner API

### `Spawner`
Location: `Game/simulation/map/spawn.py`

Purpose:
Creates entities in valid world tiles using a registry-driven spawn system.

Signature:

```python
class Spawner:
    def __init__(self, world, terrain_layer):
        ...
```

Key methods:

```python
is_tile_available(x, y, terrain_id=0, ignore_entity=None, valid_parents=None) -> bool
```
Checks whether a tile is suitable for spawning.

```python
get_valid_spawn_tile(position=None, terrain_id=0, fallback_search=None, ignore_entity=None, valid_parents=None)
```
Returns a valid position if available, otherwise `None`.

```python
find_grass_tile(pos=None)
find_water_tile(pos=None)
find_tile_near_water(pos=None)
```
Find random tiles matching terrain or nearby-water conditions.

```python
spawn_entity(type_name, position=None, **kwargs)
```
Dispatches to the matching spawn function in `spawn_registry`.

Spawn registry entries include:
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

Typical spawn behavior:
- validates tile eligibility
- creates entity ID
- attaches required components
- returns the entity ID

---

## 4. System APIs

### `MovementSystem`
Location: `Game/ecs/systems/movement.py`

Purpose:
Moves entities along a precomputed path.

Signature:

```python
class MovementSystem:
    def __init__(self, world):
        ...

    def update(self):
        ...
```

Behavior:
- reads entities with `Position`, `MoveTo`, and `Path`
- consumes the next node in the path
- updates world spatial indexing
- removes `MoveTo` when path is complete

---

### `JobSystem`
Location: `Game/ecs/systems/job.py`

Purpose:
Executes the currently selected job for each entity.

Signature:

```python
class JobSystem:
    def __init__(self, world, map, spawnner, growthSystem):
        ...

    def update(self):
        ...
```

Key job handlers:

```python
Gather(entity, job)
Consume(entity, job)
Tansfer(entity, job)
Craft(entity, job)
Build(entity, job)
Explore(entity, job)
Plant(entity, job)
PlaceBlueprint(entity, job)
```

Behavior:
- picks the highest-priority active job
- routes the job to the correct handler
- updates entity state and inventories as jobs resolve
- may spawn new entities or destroy targets when tasks complete

Notes:
- `PlaceBlueprint` is described in code-driven flow but may be partially implemented depending on the active branch.
- `Tansfer` is spelled this way in the current file and is kept as-is for consistency with source code.

---

### `AISystem`
Location: `Game/ecs/systems/ai.py`

Purpose:
Decides what jobs to assign to entities based on rule priorities.

Signature:

```python
class AISystem:
    def __init__(self, world, map_data, spawner, perception):
        ...

    def update(self):
        ...

    def assign_optimal_job(self, entity):
        ...

    def apply_job_stack(self, entity, jobs):
        ...

    def pseudo_update(self):
        ...
```

Behavior:
- checks entities with `Hunger`
- skips if the entity already has a `Job`
- tries survival and productivity rule sets in order
- converts generated job dicts into `Job` components

Rule order:
- `Survival`
- `Productivity`

---

### `GrowthSystem`
Location: `Game/ecs/systems/growth.py`

Purpose:
Manages age-driven entity lifecycle and respawn logic.

Signature:

```python
class GrowthSystem:
    def __init__(self, world, spawner):
        ...

    def update(self):
        ...

    def add_respawn(self, type_name, pos):
        ...
```

Behavior:
- each tick checks `Growth` age
- destroys expired entities
- may spawn a next-phase entity
- queues respawn for resource types

---

### `HungerSystem`
Location: `Game/ecs/systems/hunger.py`

Purpose:
Applies hunger decay to entities.

Signature:

```python
class HungerSystem:
    def __init__(self, world):
        ...

    def update(self):
        ...
```

Behavior:
- for each entity with `Hunger`, decreases its value by 3 per update tick

---

### `VisionSystem`
Location: `Game/ecs/systems/vision.py`

Purpose:
Computes which nearby entities are visible to an entity based on its vision range.

Signature:

```python
class VisionSystem:
    def __init__(self, world):
        ...

    def update(self):
        ...
```

Behavior:
- reads `Vision` and `Position`
- collects all entities in a square radius
- writes visible entity IDs to the `Vision` component

---

### `PerceptionSystem`
Location: `Game/ecs/systems/perception.py`

Purpose:
Converts visible entity data into a structured perception dictionary for reasoning.

Signature:

```python
class PerceptionSystem:
    def __init__(self, world):
        ...

    def decode(self, parent_entity):
        ...
```

Returns:

```python
{
    entity_id: {
        "distance": int,
        "type": "EntityType"
    }
}
```

---

## 5. Component API

All components are simple data containers. They live under `Game/ecs/components/`.

### `Position`
```python
class Position:
    def __init__(self, x, y):
        ...
```
Fields:
- `x`
- `y`

### `Inventory`
```python
class Inventory:
    def __init__(self, items=None):
        ...
```
Fields:
- `items`: dictionary of item names to counts

### `Job`
```python
class Job:
    def __init__(self, job=None):
        ...
```
Fields:
- `job`: list of job dicts with priority and metadata

### `Hunger`
```python
class Hunger:
    def __init__(self, hunger):
        ...
```
Fields:
- `hunger`

### `Type`
```python
class Type:
    def __init__(self, type):
        ...
```
Fields:
- `type`

### `State`
Represents the current action state of an entity, such as `idle` or `Gathering Tree`.

### `Vision`
Stores nearby entities and range information.

### `Growth`
Tracks age and lifespan, used by lifecycle and respawn systems.

### `Renderable`
Stores visual metadata for entity rendering, such as image file and sprite size.

---

## 6. Data API

### `ENTITIES`
Location: `Game/data/entities.py`

Purpose:
Static metadata for all world entities.

Example shape:

```python
ENTITIES = {
    "Tree": {
        "Health": (80, 100),
        "Inventory": {"Wood": (10, 20), "Food": (1, 10)},
        "interval": 4,
        "death_age": (25, 30),
        "respawn_interval": (30, 50),
        "size": (1, 2)
    }
}
```

Used by:
- `Spawner`
- `GrowthSystem`
- job and resource logic

### `ITEMS`
Location: `Game/data/items.py`

Purpose:
Defines item consumption effects.

Example:

```python
ITEMS = {
    "Food": {
        "consume": {
            "Hunger": 30
        }
    }
}
```

### `RECIPES`
Location: `Game/data/recipes.py`

Purpose:
Defines crafting formulas.

Example:

```python
RECIPES = {
    "StoneAxe": {
        "Input": {"Stone": 2, "Wood": 3},
        "Output": {"StoneAxe": 1},
        "Time": 10
    }
}
```

### `BLUEPRINTS`
Location: `Game/data/blueprints.py`

Purpose:
Defines structures that can be built.

Example:

```python
BLUEPRINTS = {
    "House": {
        "Input": {"Wood": 4, "Stone": 4},
        "Entity": "House",
        "Time": 30,
        "Size": (3, 3)
    }
}
```

---

## 7. Rendering API

### `RenderSystem`
Location: `Game/interface/render_system.py`

Purpose:
Main rendering orchestration layer.

Signature:

```python
class RenderSystem:
    def __init__(self, world, terrain_layer, screen, map_surface, tile_size, camera):
        ...

    def update(self, state):
        ...
```

Responsibilities:
- draw terrain and entities
- blit map to the main screen
- render top and sidebar UI
- support debug overlays via `state`

### `Camera`
Location: `Game/interface/camera.py`

Purpose:
Moves the viewport to follow world coordinates or selected entities.

Signature:

```python
class Camera:
    def __init__(self, viewport_width, viewport_height, map_width_pixels, map_height_pixels):
        ...

    def move(self, dx, dy):
        ...

    def update_target(self, target_x_pixels, target_y_pixels):
        ...
```

---

## 8. Utility API

### `pathfinding(start, goal, grid)`
Location: `Game/utils/pathfinding.py`

Purpose:
Computes a path across a grid using a heuristic search approach.

Signature:

```python
def pathfinding(start, goal, grid):
    ...
```

Parameters:
- `start`: tuple `(x, y)`
- `goal`: tuple `(x, y)`
- `grid`: 2D list where walkable cells are `0`

Returns:
- list of coordinates forming the route, or `None` if no route is found

---

## 9. Extension Points

The main extension points in the current project are:

1. New components under `Game/ecs/components/`
2. New systems under `Game/ecs/systems/`
3. New entity definitions under `Game/data/entities.py`
4. New jobs in `JobSystem.handlers`
5. Additional rules in `hunger_rules.py` and `work_rules.py`
6. New rendering elements under `Game/interface/`

This makes the project easy to evolve without changing the central world registry.

---

## 10. Stability Notes

The API surface is intentionally lightweight and prototypical. Some code paths are still best described as experimental or partially finished. In particular:

- some methods rely on internal conventions rather than strict typed interfaces
- several component updates are direct attribute mutation
- job handling and entity lifecycle are still evolving
- render and simulation entry points are not fully standardized yet

This is normal for an early-stage simulation project and provides clear opportunities for refactoring and hardening.

---

## 11. Summary

The project exposes a compact but useful simulation API centered on a `World` manager, component-driven entities, and rule-based systems. The main developer-facing entry points are:

- `World`
- `Spawner`
- `Map`
- `MovementSystem`
- `JobSystem`
- `AISystem`
- `GrowthSystem`
- `VisionSystem`
- `RenderSystem`

Together, these form the primary “public” surface of the simulation engine.
