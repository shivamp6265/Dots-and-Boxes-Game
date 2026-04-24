# Dots-and-Boxes-Game

A graphical implementation of the classic **Dots and Boxes** game built using **Python Tkinter** and **NumPy**. The project includes two gameplay modes:

- Human vs Human (HvH)
- Human vs Robot (HvR)


## Overview

Dots and Boxes is a turn-based strategy game where players take turns drawing lines between dots on a grid. Whenever a player completes the fourth side of a box, they claim it and earn a point plus an extra turn.

This project features:
- Interactive GUI built with Tkinter
- Two game modes (PvP and PvAI)
- Score tracking system
- Turn-based logic with automatic box detection
- Simple AI opponent with greedy strategy


## Features

### Human vs Human (HvH)
- Two players play locally on the same device
- Alternating turns
- Automatic detection of completed boxes
- Score tracking for both players
- Game-over detection with restart option

### Human vs Robot (HvR)
- Play against an AI opponent
- AI logic includes:
  - Prioritizing moves that complete boxes
  - Avoiding moves that create vulnerable 3-sided boxes
  - Random fallback for safe moves
- Smooth AI turn delay for better UX


## Technologies Used

- Python 3
- Tkinter (GUI framework)
- NumPy (grid/state management)


## How to Run

### Install dependencies
```pip install numpy```

### Run Human vs Robot mode
```python human_vs_robot.py```

### Run Human vs Human mode
```python human_vs_human.py```