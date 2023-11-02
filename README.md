# Hitory game
Hitory game python implementation with g2d graphics library.

| Starting board              | Finished puzzle          |
| ---------------------- | ---------------------- |
| [![Starting board](https://www.conceptispuzzles.com/picture/11/1369.gif)](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/hitori/rules) | [![Starting board](https://www.conceptispuzzles.com/picture/11/1369.gif)](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/hitori/rules) |


## How to play
Hitori is played with a grid of squares or cells, with each cell initially containing a number. The game is played by eliminating squares/numbers and this is done by blacking them out. The objective is to transform the grid to a state wherein all three following rules are true:
- no row or column can have more than one occurrence of any given number
- black cells cannot be horizontally or vertically adjacent, although they can be diagonal to one another.
- the remaining numbered cells must be all connected to each other, horizontally or vertically.
More info at [Wikipedia](https://en.wikipedia.org/wiki/Hitori).

## How to run
Simply move in the project folder and run the following command:
```
python hitory.py
```

## Features
- [c] Clear all cells
- [u] If two circles have the same value, one is set to black
- [s] Play automatically the next move
- [w] Solve the game automatically
- [h] Draw automatically circles adjacent to black cells
- [?] Manual with shortcuts and rules
- [q] Quit the manual

