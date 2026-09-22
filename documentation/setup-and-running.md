# Setup and Running Guide

## Requirements

The project depends on Python and a few packages listed in `requirements.txt`.

### Required packages

- Python 3.x
- numpy
- pygame

Install them with:

```bash
pip install -r requirements.txt
```

---

## Running the Project

From the project root:

```bash
cd /path/to/SimVille
python Game/main.py
```

If you want to use the alternate test harness:

```bash
python Game/test.py
```

---

## Important Runtime Note

The current game entry point in `Game/main.py` is written as a longer game loop and expects a Pygame window environment. This means the system is designed for local desktop execution rather than a web or headless server context.

---

## Example Boot Sequence

The application does the following when launched:

1. creates a `World`
2. creates a `Map`
3. creates a `Spawner`
4. sets up systems such as `MovementSystem`, `JobSystem`, `AISystem`, and `HungerSystem`
5. spawns initial resources and NPCs
6. runs the main update/render loop

---

## Environment Notes

Because the project writes logs to a file, ensure the working directory is valid before running the program. It writes to `app.log` at the project root or current runtime context depending on how it is launched.

---

## Local Development Tips

- use a virtual environment for isolating dependencies
- run the game from the repository root for predictable asset paths
- verify asset files exist in the `Game/assets` folder before debugging rendering issues
- if the display is not expected, check whether the game is starting in a graphical environment

---

## Common Troubleshooting

### Missing packages
Run:

```bash
pip install -r requirements.txt
```

### Rendering issues
Check whether the assets folder exists and whether image file names match the references in the code.

### Entity or world logic issues
Use the logging output in `app.log` to inspect component updates and simulation events.

---

## Future Run Modes

The project may later evolve toward:

- more robust CLI options
- richer simulation settings
- configuration files for world seed or map size
- dependency management via poetry or pip-tools

For now, the project is a direct Python application.
