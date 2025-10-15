# Platformer Game

A simple 2D platformer made with Pygame Zero.

## Requirements

- Python 3.7 or higher
- Pygame Zero library

## Libraries

-pygame zero

## Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install Pygame Zero**:
   Open your terminal/command prompt and run:
```bash
   pip install pgzero
```

## Running the Game

### Method 1: Using pgzrun (Recommended)
Navigate to the game folder in your terminal and run:
```bash
pgzrun pgzgame.py
```

### Method 2: Using Python directly
```bash
python pgzgame.py
```

### Method 3: Windows - Double Click
Simply double-click `pgzgame.py` if Python is properly configured.

## File Structure

Make sure your folder contains:
```
pgzero/
├── pgzgame.py              # Main game file
├── level_data.py           # Level design
├── images/                 # Game sprites
└── sounds/                 # Sound effects and music
```

## Controls

- **← →** Arrow Keys - Move left/right
- **Space** - Jump
- **Mouse** - Click menu buttons

## Objective

Collect coins and reach the flag while avoiding enemies. Good luck!

## Troubleshooting

**"No module named 'pgzero'"**
- Run: `pip install pgzero`

**"No module named 'level_data'"**
- Make sure `level_data.py` is in the same folder as `pgzgame.py`

**Missing images or sounds**
- Ensure `images/` and `sounds/` folders exist with all required files