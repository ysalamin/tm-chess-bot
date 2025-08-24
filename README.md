# Chess AI Bot

A chess engine with a customizable AI opponent, created as part of a Swiss "Travail de Maturité" (final high school project). It's actually my first real project.



## Getting Started

Instructions on how to set up and run the project locally.

### Prerequisites

This project requires Python 3 and the following modules:
* `pygame`
* `python-chess`

### Installation

1.  Clone the repository to your local machine:
    ```bash
    git clone https://github.com/ysalamin/tm-chess-bot.git
    ```
2.  Install the required packages using pip:
    ```bash
    pip install pygame python-chess
    ```

### Running the Game

To start a game, run the `main.py` file from the terminal:
```bash
python main.py

---
## Configuration

You can easily customize the game by modifying the constants at the top of the `main.py` file:

* **`CALCULATION_DEPTH`**: Sets the AI's difficulty by controlling its search depth.
    * `2`: Beginner
    * `3`: Medium
    * `4`: Hard (can be slow)

* **`PLAYER_COLOR`**: Determines the color you play as.
    * `True`: Player is White.
    * `False`: Player is Black.
