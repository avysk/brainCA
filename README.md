# Brian's Brain

A 2D cellular automaton simulation implementing **Brian's Brain**, a cellular automaton devised by Brian Silverman.

## About

Brian's Brain is a three-state cellular automaton that produces complex, brain-like patterns from simple rules. The simulation starts with a sparse random seed and evolves into intricate wave-like structures.

## Rules

Each cell exists in one of three states:

| State      | Color        | Transition                                   |
|------------|--------------|----------------------------------------------|
| Active     | Orange       | Becomes cooldown in the next generation      |
| Cooldown   | Yellow-green | Becomes passive in the next generation       |
| Passive    | Dark cyan    | Becomes active if exactly 2 neighbors are active |

The rules create self-propagating patterns where "waves" of activity travel across the grid.

## Installation

```bash
pip install numpy pygame
```

## Usage

```bash
python brain.py
```

Close the window to exit. A screenshot will be saved to `out.png`.

## Configuration

Adjust these constants at the top of `brain.py`:

| Constant  | Default | Description                              |
|-----------|---------|------------------------------------------|
| `SIZE`    | 500     | Grid size (500 × 500 cells)              |
| `FRAMERATE`| 30     | Target frames per second                 |
| `P_ACTIVE`| 0.004   | Initial probability of a cell being active|

## Requirements

- Python 3
- NumPy
- Pygame

## Screenshot

![Example](ex.png)

## License

BSD 2-Clause
