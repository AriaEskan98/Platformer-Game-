# Platformer Game

A simple 2D platformer made with Pygame Zero.

## Requirements

- Python 3.7 or higher
- Pygame Zero library

## Installation

### 1. Install Python (if not already installed)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

**Mac:**
- Python 3 is usually pre-installed on Mac
- Check by opening Terminal and running: `python3 --version`
- If not installed, download from [python.org](https://www.python.org/downloads/)

**Linux:**
- Python 3 is usually pre-installed
- If not, run: `sudo apt-get install python3 python3-pip`

### 2. Install Pygame Zero

Open your terminal/command prompt and run:

**Windows:**
```bash
pip install pgzero
```

**Mac/Linux:**
```bash
pip3 install pgzero
```

## Running the Game

Navigate to the game folder in your terminal and run:

**Windows:**
```bash
pgzrun pgzgame.py
```
or
```bash
python pgzgame.py
```

**Mac/Linux:**
```bash
pgzrun pgzgame.py
```
or
```bash
python3 pgzgame.py
```

**Windows (Alternative):**
Simply double-click `pgzgame.py` if Python is properly configured.

## File Structure

Make sure your folder contains:
```
platformer-game/
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
- Windows: `pip install pgzero`
- Mac/Linux: `pip3 install pgzero`

**"No module named 'level_data'"**
- Make sure `level_data.py` is in the same folder as `pgzgame.py`

**Missing images or sounds**
- Ensure `images/` and `sounds/` folders exist with all required files

**Mac: "command not found: pgzrun"**
- Use `python3 pgzgame.py` instead