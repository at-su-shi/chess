# Simple Chess AI Demo

This project is a simple **AI vs. AI chess demo** built with Python and Pygame.  
The game automatically starts, and both sides are controlled by the computer using a basic **Minimax algorithm** with a simple evaluation function.  
It is designed for educational/demonstration purposes, not as a full-featured chess engine.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/at-su-shi/chess.git
   cd chess


## Usage
Run the game with:
python3 chess_main.py

The game launches automatically, and the two AIs play against each other.
Messages are displayed in English using the default Pygame font.
Piece images are included in the images/ folder.


## Known Limitations
No in-game restart/quit buttons
The game window must be closed via the OS (the "X" button).
To start a new game, re-run chess_main.py.
Draw rules are limited
Implemented: checkmate, stalemate
Not implemented: threefold repetition, fifty-move rule
As a result, the engine may endlessly repeat the same moves instead of declaring a draw.
No resignation
Since the game is AI vs. AI only, resignation is not part of the rules.
Simplistic AI
The Minimax algorithm is implemented in its most basic form, primarily as a demonstration.
It does not include optimizations such as alpha-beta pruning or advanced evaluation functions.


## File Structure
chess/
├─ images/                  # Piece images
├─ chess_ai.py              # Minimax AI
├─ chess_engine.py          # Board logic and rules
├─ chess_main.py            # Entry point
├─ chess_ai_piece_scores.py # MinMax Evaluation
├─ requirements.txt
├─ README.md
└─ .gitignore


## License
This project is released under the MIT License.
Piece images in images/ are included under their respective licenses.
No proprietary fonts are bundled. The game uses the default pygame font.

