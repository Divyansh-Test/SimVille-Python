# SimVille-Python Documentation

## Overview

SimVille-Python is a multi-agent simulation project built in Python. The project models a small village-like world in which entities such as trees, stones, NPCs, and construction sites exist in a shared map. The simulation uses an entity-component-system (ECS) architecture to manage world state, movement, growth, hunger, jobs, and perception.

This repository currently represents a prototype / early-stage simulation. It is designed as a playground for experimenting with AI-driven behavior, automating resource collection, and simulating a small social/economic loop in a grid world.

## Repository Purpose

The project aims to:

- simulate a tile-based world with terrain and entities
- represent agents as entities with components
- let entities react to hunger, growth, and tasks
- model jobs such as gathering, building, and exploring
- render the world and state in a terminal or Pygame-based interface

## Reality Check

While the root README describes the project as using AI-driven agents, the current implementation is primarily heuristic and rule-based rather than a trained machine-learning model. Much of the decision-making comes from job rules and task generators in the `ecs/systems` package, not from a formal ML model.

This is an important architectural fact for contributors: the current project is a simulation engine with rule-driven agent behavior.

---

## High-Level Architecture

The project is organized around four core ideas:

1. Entities are IDs that exist in the world.
2. Components are data attached to entities.
3. Systems update entities based on their components.
4. The world tracks entity positions, inventories, states, and relationships.

This architecture makes the simulation flexible and easy to extend.

---

## Project Goals

The intended direction of the project includes:

- richer world simulation
- more realistic NPC behavior
- resource chains and crafting
- building construction and farm systems
- world interactions driven by AI or rule logic
- a more polished user interface and camera system

---

## Quick Start Summary

To run the project:

1. install dependencies from `requirements.txt`
2. ensure you are in the project root
3. run the app entry point from `Game/main.py` or the custom game loop in `Game/test.py`

The active game loop is currently centered on the code in `Game/main.py` and uses Pygame-based rendering.

---

## Documentation Map

This documentation set is organized as follows:

- [architecture.md](architecture.md): explains ECS design and system responsibilities
- [project-structure.md](project-structure.md): explains files and folders
- [setup-and-running.md](setup-and-running.md): install and execution instructions
- [system-reference.md](system-reference.md): details the major systems and components

---

## Current Project Status

This repository is in an early development state. Some parts are actively evolving and some code paths still show prototype or partially finished logic.

Expected characteristics of the current state:

- entity spawning and map generation work
- resource gathering and building logic exist
- pathfinding is present but simplistic
- world behavior is rule-driven, not yet deeply data-driven
- some systems are incomplete or experimental

---

## Suggested Contribution Areas

Good starting points for future work include:

- better job prioritization
- pathfinding and movement robustness
- additional resource types and recipes
- clearer AI decision policies
- world state persistence and save/load
- improved rendering and UI
- tests for ECS logic and job execution

---

## Summary

SimVille-Python is a compact ECS simulation project focused on constructing a village-like world with autonomous characters and resource chains. Although the project is early-stage, the foundation is already present: a world, entities, systems, map generation, AI-like logic, rendering, and data-driven entity definitions.

This documentation aims to make the codebase understandable and easier to extend.
