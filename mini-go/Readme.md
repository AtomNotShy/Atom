# Mini-go
## Author: Tong Zhou
This project developed a agent to play a small version of the Go game, called Go-5x5 or Little-Go, that has a reduced board size of 5x5.
### Rule1: The Liberty Rule
Every stone remaining on the board must have at least one open point, called a liberty, directly orthogonally adjacent (up, down, left, or right), or must be part of a connected group that has at least one such open point (liberty) next to it. Stones or groups of stones which lose their last liberty are removed from the board (called captured).

Example 1:The white stone is captured after Black plays at position 1, because its directly orthogonally adjacent points are occupied.
![image](https://github.com/AtomNotShy/Atom/blob/master/mini-go/images/example1.png)

Example 2:The 3 white stones are captured as a connected group.
![image](https://github.com/AtomNotShy/Atom/blob/master/mini-go/images/example2.png)

Example 3. The two groups of white stones are captured.
![image](https://github.com/AtomNotShy/Atom/blob/master/mini-go/images/example3.png)

Example 4. This example illustrates the rule that a capturing stone need not have a liberty until the captured stones are removed.
![image](https://github.com/AtomNotShy/Atom/blob/master/mini-go/images/example4.png)

### Rule 2: The “KO” Rule
For the position shown on the left board above, Black can capture the white stone by a play at position a. The resulting position is shown on the right board above. Without a KO rule, in this position White could recapture the Black stone at position b, reverting to the position shown on the left, and then Black could also recapture. If neither player gave way, then we would have Black a, White b, Black a, White b, ..., repeated ad infinitum, stalling the progress of the game. This situation is known as KO.

![image](https://github.com/AtomNotShy/Atom/blob/master/mini-go/images/KO.png)

### Komi
Because Black has the advantage of playing the first move, awarding White some compensation is called Komi. This is in the form of giving White a compensation of score at the end of the game. In this game (a board size of 5x5), Komi for the White player is set to be 5/2 = 2.5.

### End of Game
A game ends when it reaches one of the four conditions:
- When a player’s time for a single move exceeds the time limit (See Section 6. Notes and Hints).
- When a player makes an invalid move (invalid stone placement, suicide, violation of KO rule).
- When both players waive their rights to move. Namely, two consecutive passes end the game.
- When the game has reached the maximum number of steps allowed. In this homework (a board
size of 5x5), the maximum number of steps allowed is (5*5)-1 = 24.

### Battle
try  `sh build.h` to play with random agent
