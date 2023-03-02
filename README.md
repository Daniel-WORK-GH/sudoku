# Sudoku

Puzzeles taken from https://www.printable-sudoku-puzzles.com/wfiles/

### instructions
The game contains 3 difficulties:
- easy
- medium
- hard
and is set on easy, a simple change in the main.py will change 
the difficulty.

the objective is simple - fill the board with numbers 1 - 9 such that:
- every row contains only one occurrence of each number.
- every column contains only one occurrence of each number.
- every 3x3 grid contains only one occurrence of each number.

### Controls
Right click - write selected number on empty spots, will delete
              if no number is selected
              
Left click - delete number

numbers marked green are the starting numbers and cant be changed.
black numbers can be deleted and rewritten.

each time you select a number to write using the bar at the bottom
each occurrence of the selected number will turn red on screen for
easier gameplay.

### Technical data
selector.py - will select a random unplayed board from the text files
              based on the current selected difficulty

sudoku.py - all the game logic and graphics

main.py - initial start of the program

each difficulty file in the boards folder contains 10,000 puzzles

![example1](https://user-images.githubusercontent.com/120199463/222400638-8bb1cf86-027e-4420-bf50-3d872d59ea88.jpg)
