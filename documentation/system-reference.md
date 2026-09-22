# System and Module Reference

## World System

### `World`
File: `Game/ecs/world.py`

This is the central registry for the simulation. It manages:

- entity creation
- component storage
- grid occupancy
- component lookup
- entity destruction
- nearest-entity search

### Main responsibilities

- `create_entity()`
- `add_component()`
- `update_component()`
- `remove_component()`
- `get_component()`
- `has_component()`
- `get_entity_with()`
- `destroy_entity()`
- `find_nearest_entity()`

---

## Map and Spawn Systems

### `Map`
File: `Game/simulation/map/map.py`

Creates a grid-based terrain layer for the world.

### `Spawner`
File: `Game/simulation/map/spawn.py`

Handles:

- spawn validation
- world occupancy checks
- tile selection for resources and buildings
- entity creation with appropriate components

Key methods include:

- `is_tile_available()`
- `get_valid_spawn_tile()`
- `find_grass_tile()`
- `find_water_tile()`
- `find_tile_near_water()`
- `spawn_entity()`

---

## AI and Game Logic

### `AISystem`
File: `Game/ecs/systems/ai.py`

Responsibilities:

- evaluate hunger state
- rank planned actions by priority
- assign tasks to entities
- use the rule sets for survival and productivity

### `JobSystem`
File: `Game/ecs/systems/job.py`

Processes active jobs for entity behaviors.

Covered behaviors include:

- gathering resources
- consuming food
- transferring inventory
- crafting items
- building structures
- exploring
- planting crops
- placing blueprints

### `HungerSystem`
File: `Game/ecs/systems/hunger.py`

Lowers hunger each tick for entities with a hunger component.

### `GrowthSystem`
File: `Game/ecs/systems/growth.py`

Controls progression, aging, death, respawn, and phase transitions.

### `MovementSystem`
File: `Game/ecs/systems/movement.py`

Moves entities along a calculated path and keeps their `position_to_entity` map consistent.

### `VisionSystem`
File: `Game/ecs/systems/vision.py`

Finds entities within the vision radius and updates the `Vision` component with nearby entity IDs.

### `PerceptionSystem`
File: `Game/ecs/systems/perception.py`

Transforms nearby entity data into information useful for AI decision-making.

---

## Rule Modules

### `hunger_rules.py`
This file defines hunger-driven behavioral rules, especially:

- eating if food is available
- gathering food if hunger is high
- exploring when no food is available

### `work_rules.py`
This file defines productivity-focused behavior such as:

- building a house
- placing blueprint constructions
- planting crops
- transfer of resources
- exploration fallback

The code indicates a design intention to prioritize building and production tasks, while the current active rules are still limited.

---

## Rendering Modules

### `RenderSystem`
File: `Game/interface/render_system.py`

High-level render orchestration for the world and UI.

### `render_map.py`
Draws terrain and entities with optional debug overlays for:

- vision radius
- path visualization
- target line
- job or state labels

### `camera.py`
Controls viewport scrolling and camera focus over the world.

### `render_ui.py`
Handles the top bar / sidebar interface for the simulation.

---

## Components

Some of the most important components are:

### `Position`
Stores x/y tile coordinates.

### `Inventory`
Stores a dictionary of item counts.

### `Type`
Stores the entity kind such as `Tree`, `Stone`, or `Human`.

### `Health`
Tracks health or durability.

### `Hunger`
Tracks hunger value.

### `Job`
Stores the job list assigned to an entity.

### `Vision`
Tracks visible nearby entities.

### `Growth`
Tracks age and lifecycle timing.

### `State`
Tracks the current action or status string.

### `Renderable`
Stores sprite metadata such as image file name or sprite size.

---

## Data Definitions

### `data/entities.py`
Defines many of the world’s entity profiles.

### `data/items.py`
Defines item consumption effects.

### `data/recipes.py`
Defines crafting recipes.

### `data/blueprints.py`
Defines building requirements and blueprint metadata.

---

## Summary

The system reference above covers the project’s main modules and responsibilities. The design is intentionally modular, and the codebase is organized around a small ECS core, a map + spawn layer, a simulation logic layer, and a rendering layer.

This organization is a good foundation for future growth, especially if the project expands into richer world simulation and more advanced NPC reasoning.
