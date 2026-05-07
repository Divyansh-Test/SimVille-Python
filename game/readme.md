# This is the file that stores the symbol means what.
## Tiles
* =land
* =stones
* =walls

# delete it after it all happens.
2D grid (like 20x20)
Each cell = tile (grass, water, stone)
Print it in terminal (ASCII)

Hint thinking:

World = data, not visuals
Use arrays or vectors
Don’t care about graphics yet
Phase 2: Entities (life begins)

Goal: something exists and moves.

6

Build this:

One creature (player or dwarf)
Position (x, y)
Random or keyboard movement

Think:

Separate “world” and “entity”
Don’t hardcode behavior into the map
Phase 3: Time & Simulation (this is where most fail)

Goal: world updates every tick.

5

Build this:

Game loop (tick system)
Each tick:
move entities
update world

Critical mindset:

Everything = system update
No “magic events”, only rules
Phase 4: Needs & Behavior (real DF starts here)

Goal: creatures have internal state.

7

Build this:

Hunger value
If hungry → search food
If no food → wander

Think deeper:

Behavior = rules + state
Not “if else hell”, but systems interacting
Phase 5: Resources & Jobs

Goal: actual gameplay loop.

5

Build this:

Trees → wood
Dwarf → chop tree
Store resources

Key idea:

Jobs should exist independently
Entities pick jobs, not vice versa
Phase 6: Scale (this breaks weak designs)

Goal: 50–100 entities without chaos.

8

Now you’ll feel pain:

Slow performance
Messy code
Bugs everywhere

Good. That’s where real learning starts.



This is patani kyu but i am trying to make this repo pull to my local and let ssee do it sync any changes.
