# Connect AI — Minimax with Alpha-Beta Pruning

A Python implementation of **Connect** (a generalised version of Connect 4) featuring an AI opponent powered by the minimax algorithm. The AI supports both plain minimax and minimax with alpha-beta pruning, and uses a **transposition table** to cache previously evaluated board states for improved performance.

The board size and win condition are fully configurable, making it easy to test across different game setups.

---

## Features

- **Minimax AI** — explores the game tree to find the optimal move
- **Alpha-Beta Pruning** — significantly reduces the number of nodes evaluated without affecting the result
- **Transposition Table** — caches board states to avoid redundant evaluations
- **Heuristic Evaluation** — scores non-terminal board states based on streaks, threats, and center control
- **Configurable Board** — set any number of rows, columns, and pieces-in-a-line required to win
- **Multiple Opponent Modes** — play against the AI, a random bot, or control a player yourself

---

## Project Structure

```
├── player.py         # AI player implementing minimax and alpha-beta pruning
├── board.py          # Board representation and game logic
├── game.py           # Game loop, cycles between players
├── runGame.py        # Entry point for running and evaluating games
├── randomPlayer.py   # Baseline opponent that picks random valid moves
├── realPlayer.py     # Human player, input via terminal
```

---

## Getting Started

### Prerequisites

- Python 3.x
- `notifypy` (optional, used for desktop notifications when a run finishes)

```bash
pip install notifypy
```

### Running a Game

Edit `runGame.py` to configure your game setup, then run:

```bash
python runGame.py
```

Key settings in `runGame.py`:

```python
rows = 5          # Number of rows on the board
columns = 3       # Number of columns on the board
winNum = 3        # Number of pieces in a line required to win
totalGames = 2    # Number of games to simulate
```

---

## How It Works

### Minimax

The AI uses minimax to explore possible future game states up to a set depth. It assumes the opponent always plays optimally, then picks the move with the best guaranteed outcome.

### Alpha-Beta Pruning

Alpha-beta pruning cuts branches of the game tree that can't possibly affect the final decision, dramatically reducing the number of nodes expanded — especially on larger boards.

### Transposition Table

Board states are hashed as strings and stored in a dictionary. If the same board position is reached via different move sequences, the cached result is returned immediately instead of re-evaluating the subtree.

### Heuristic Evaluation

When the search depth is exhausted on a non-terminal state, the board is scored based on:
- Length of consecutive streaks for the AI and opponent
- Opponent threats (near-winning positions)
- Piece proximity to the center columns (strategically stronger positions)

---

## Player Modes

| Class | Description |
|---|---|
| `Player` | AI using minimax / alpha-beta |
| `RandomPlayer` | Picks a random valid column each turn |
| `RealPlayer` | Human input via terminal |

You can mix and match these in `runGame.py`:

```python
p1 = player.Player("X")               # AI as player 1
p2 = randomPlayer.RandomPlayer("O")   # Random bot as player 2

g = game.Game(p1, p2, rows, columns, winNum)
g.playGame(True)   # True = use alpha-beta, False = plain minimax
```

---

## Stats & Output

After each run, the following are printed to the console:

- Win / loss / draw counts and win rate
- Total and average time per game
- Average nodes expanded
- Average branches pruned (alpha-beta only)

---

## Example Output

```
Games run: 10
Rows: 5 | Columns: 4 | Win num: 3 | Depth: 5

Wins: 9 | Losses: 0 | Draws: 1 | Winrate: 90.0%

Total Time: 12.43s | Average Time: 1.24s | Std Dev: 0.31s
Average nodes expanded: 48203 | Std Dev: 5012
Average pruned: 19841 | Std Dev: 3204
```
