# Project Structure

## Top-Level Layout

```text
SimVille/
├── README.md
├── requirements.txt
├── documentation/
├── Game/
│   ├── config.py
│   ├── logger_config.py
│   ├── main.py
│   ├── test.py
│   ├── assets/
│   ├── data/
│   ├── ecs/
│   ├── interface/
│   ├── simulation/
│   └── utils/
└── .gitignore
```

---

## Root Files

### README.md
Overview for the repository, including the project description and goals.

### requirements.txt
Python dependency list. Currently includes:

- numpy
- pygame

---

## Game Package

### config.py
Contains global configuration values for map sizing, window size, viewport values, and UI layout.

### logger_config.py
Sets up file logging for the application. Logs are written to `app.log`.

### main.py
The main runtime loop for the simulation. This is the application entry point for the Pygame-based game.

### test.py
Alternate or experimental simulation script. It appears to be a test harness or earlier game loop reference.

---

## Data Layer

### data/entities.py
Defines entity metadata for trees, stones, humans, farms, and seedlings. Includes health ranges, resource inventories, timing values, and lifecycle definitions.

### data/items.py
Defines consumable items and their effects.

### data/recipes.py
Defines crafting recipes and required inputs/outputs.

### data/blueprints.py
Defines building blueprints and their inputs.

---

## ECS Layer

### ecs/world.py
The world manager and central data structure for all entities and components.

### ecs/component_registry.py
Maps important component names to their classes and relevant attribute metadata.

### ecs/components/
Contains component classes:

- `attack_power.py`
- `attack_range.py`
- `blueprint.py`
- `growth.py`
- `health.py`
- `hunger.py`
- `inventory.py`
- `job.py`
- `move_to.py`
- `path.py`
- `position.py`
- `renderable.py`
- `stamina.py`
- `state.py`
- `thrist.py`
- `type.py`
- `vision.py`

These are the primary data types of the world.

### ecs/systems/
Contains the simulation logic:

- `ai.py`: high-level decision selection
- `growth.py`: age and lifecycle logic
- `hunger.py`: hunger drain logic
- `hunger_rules.py`: hunger-driven rule generation
- `job.py`: jobs and task execution
- `movement.py`: entity movement
- `perception.py`: visible entity encoding
- `vision.py`: visible entity detection
- `work_rules.py`: productivity and exploration rules

---

## Simulation Layer

### simulation/map/

- `generator.py`: terrain generation logic
- `map.py`: world map wrapper
- `spawn.py`: entity spawning logic and valid tile checks

This layer handles map generation and spawning of entities in valid tiles.

---

## Interface Layer

### interface/

- `camera.py`: camera position management
- `curse_render.py`: terminal rendering logic
- `render_map.py`: rendering of terrain and sprites
- `render_system.py`: high-level rendering orchestration
- `render_ui.py`: HUD and controls

This is the presentation layer for the simulation.

---

## Utilities

### utils/pathfinding.py
Contains pathfinding logic for the tile-based map.

---

## Assets

### assets/
Holds visual resources such as images for terrain and entities. This folder is used by the rendering layer.

---

## Summary

The project is split into clean conceptual layers:

- data definitions
- ECS core
- simulation systems
- rendering and UI
- map generation and spawning
- utility logic

That structure makes the project approachable, even though some systems are still prototypical.
