# Parallel-Universes Checkers

#### Authors: Yawen Deng, Candice Chen

## Introduction

We aim to develop an interactive game, called "Parallel-Universes Checkers", which is based on the [**Checkers**](https://en.wikipedia.org/wiki/Checkers#:~:text=Checkers%20(American%20English)%2C%20also,Checkers%20is%20developed%20from%20alquerque), also known as **draughts**. We apply some new rules to the original one trying to make it more fun between players. The biggest difference is how we **EXTEND** the original board.

## Variant Rules
(Basic Rules: [**Checkers**](https://en.wikipedia.org/wiki/Checkers#:~:text=Checkers%20(American%20English)%2C%20also,Checkers%20is%20developed%20from%20alquerque))  
Two parallel-universes version of Checkers are also played on one board for two players. We want to make the most of use of the board since the original
    version of Checkers only use the dark squares. So a new universe is created in our version for players to play at the dark and
    light squares at the same time. We make it more fun based on the original rules.


1. Players are allowed to do following actions during their turn:
    * Move ONE piece at the same universe TWICE (i.e. continuous two moves); continuous captures are allowed
    * Move ONE piece on EACH universe ONCE
    * Transfer ONE piece at one universe to ANOTHER universe ONCE per turn as their first move
    * Transfering is allowed only when an opponent's pieces are 2 times more the player in that universe
    * Transfer at most 3 pieces per round
    * Only allowed to transfer to an empty square and must go to an orthogonally-adjacent square on the other universe
    * CANNOT CAPTURE at the transferring round
    * Each piece can only transfer once during the whole game process
2. Winning conditions:
    * Once a player has NO PIECES on both boards on his turn, he loses.
    * Once a player has NO STEPS AND NO TRANFER options on both boards, he loses.
    * If no capture in 100 turns and two players' pieces are completely separate in different board, the one with more pieces in his board wins
3. Draw condition:
    If two players keep chasing to each other without any capture in both boads for continuous 100 turns in total,
    we end the game as a draw.

## Goal
1. Implement Checkers with variants.
2. Design an interactive interface for users to compete with each other.
3. Develop different Machine players using Minimax algorithm.
   * Random Player - always randomly choose next step without any preference and strategy
   * Lion-King Player - eager to become a king as soon as possible 
   * Aggressive Player - tend to capture as many as possible

## Interactive Interface
![image](https://user-images.githubusercontent.com/89559531/165950259-f9ab7605-9a49-46da-83dd-1650809b0cb6.png)
We develop our game window based on the traditional checkers. When the current player chooses the piece he want to move, all the possible valid moves of the next two steps for the selected piece will be indicated by blue points. Pieces can tranfer between boards, players can disdinguish pieces' home board by theri coat. pieces initially form the left board wear gold coat, while the initially right pieces are in silver.                                                                                                      

## Analysis
### Data Structures

We use list of list to store boards' state while the coordinates of the position are stored in tuples. A tuple of dictionaries is used to store two continuous moves as the rules stated. The information of dictionary includes the pieces' positions of both iniitial and the targeted ones. The boards are also recorded in the dictionary since a transferred move could be made. The last important element is the positions of opponents when capturing happens.

#### Class
* Boards and Piece: boards states and pieces' properties (e.q. king); communicate with interface
* gameState: takes care of the rules and implements the mojority of calculations
* playGame: connects the modules above and runs the game
* randomPlayer and MinimaxPlayer: get_next_move regarding their settings

#### Critical Functions and Complexity
* `get_positions` gets the positions of every pieces of a player. It could be seen as constant time O(1) since the size of boards is fixed.
* `one_move` traverses the adjacent squares searching empty spots or valid captures. O(n`^`m) where n and m represents the number of adjacent squares because two moves are available in one turn and continuous captures is possible.
* `get_normal_moves` and `get_transferred_list` calculate the possible moves of each piece. They traverse the adjacent squares and determine whether the positions are occupied or are an valid capture. Their time complexity are both O(n`^`m) where n and m represents the number of valid moves of a single piece. 
* `get_valid_moves_piece` take a piece as input to get all valid moves interms of the three ways of possible moving options. It calls the `get_normal_moves` and `get_transferred_list` functions to get all options so it's O(n`^`m) as well.
* `get_valid_moves` iterates every pieces to get all valid moves in single turn. It's O(n) where n is the number of pieces. We could also see it as relatively fixed variable since the number of pieces are almost constant. However, there is `get_valid_moves_piece` inside and is executed for each piece, we consider the complexity would be O(n`^`m) here n and m means the number of valid moves.
* `minimax_moves` simulates the possible moves following the assigned depth dwon to the leaves of the tree. Given the game state, it traverse all the possible valid moves so it's O(n`^`m) where n and m are the number of moves if the depth is 2. The cost is expensive because of several options so we implement the alpha beta pruning to reduce unnecessary calculation. 


#### Core Algorithms
We design two Minimax players with simple evaluation. Since the valid moves in our variant Checkers significantly increase (more than 50 valid moves in a single turn is possible under the board size 6 game), we set some conditions for Minimax players (both stratigies) accoding to the stage of the game. In the first few moves, it sees the positions at the center squares as priority. If no valid moves at the center, then it will go for the moves with captuers. If there's no options meet the above two condition, it randomly chooses the moves from the list of moving one piece at both boards. Once the game stage going through, the Minimax algorithm will be implemented. At the root node of the tree, we only iterate the moves with captuers attempting to reduce the number of child nodes. 


#### Mimimax Heuristic Evaluation Function
* Lion-King Player 
score = (total pieces) - (total opponent's pieces) + (total king pieces) * 1.5 - (total opponent's king pieces) * 1.5
* Aggressive Player - tend to capture as many as possible
score = (possible single capture) + 2 * (possible continuous captures)

 
 
 
## Performance Measurement
The program runs significantly longer when we increase the board size from 4 to 6. It took a couple of minutes for Minimax to search for a best move. The following is the result of a random player playing with an Aggressive (capture) player with depth 3 for a single run. As shown on the table, `minimax_moves` is the most time consuming function since the time complexity is  O(n`^`m`^`o), which is extreme large. The `get_normal_moves` is another costly function while deepcoy is called the most times.

 
![image](https://user-images.githubusercontent.com/89559531/167251625-620e0e45-b0ad-4f5a-8c4a-c9be6fe6b495.png)




### Contribution
We build our fundamental rules and create a random player together in the first stage. Then, Yawen mainly worked on UI and Candice developed the two Minimax players. 


### Reference
* GUI https://www.youtube.com/watch?v=vnd3RfeG3NM
* Minimax pseudocode  https://www.youtube.com/watch?v=l-hh51ncgDI&t=254s
