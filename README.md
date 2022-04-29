# Parallel-Universes Checkers

#### Authors: Yawen Deng, Candice Chen

## Introduction

We aim to develop an interactive game, called "Parallel-Universes Checkers", which is based on the [**Checkers**](https://en.wikipedia.org/wiki/Checkers#:~:text=Checkers%20(American%20English)%2C%20also,Checkers%20is%20developed%20from%20alquerque), also known as **draughts**. We apply some new rules to the original one trying to make it more fun between players. The biggest difference is how we **EXTEND** the original board.

## Basic Rules
[**Checkers**](https://en.wikipedia.org/wiki/Checkers#:~:text=Checkers%20(American%20English)%2C%20also,Checkers%20is%20developed%20from%20alquerque)


## Variant Rules

Two parallel-universes version of Checkers are also played on one board for two players. We want to make the most of use of the board since the original
    version of Checkers only use the dark squares. So a new universe is created in our version for players to play at the dark and
    light squares at the same time. We make it more fun based on the original rules.


1. Players are allowed to do following actions during their turn:
    * ove ONE piece at the same universe TWICE (i.e. continuous two moves); continuous captures are allowed
    * move ONE piece on EACH universe ONCE
    * transfer ONE piece at one universe to ANOTHER universe ONCE per turn as their first or second move
    * only allowed to transfer to an empty square and must go to an orthogonally-adjacent square on the other universe
    * CANNOT CAPTURE at the transferring round
2. Winning conditions:
    * Once a player has NO PIECES on both boards on his turn, he loses.
    * Once a player has NO STEPS AND NO TRANFER options on both boards, he loses.
3. Draw condition:
    If two players keep chasing to each other without any capture for continuous 50 turns in total,
    we end the game as a draw.

## Purpose
1. Implement variant rules to Checkers.
2. Design an interactive interface for users to compete with each other.
3. Develop different Machine players using Minimax algorithm.
   * Random Player - always randomly choose next step without any preference and strategy
   * Lion-King Player - eager to become a king as soon as possible (Does it remind you the song _"I Just Can't Wait to Be King"_?)
   * Aggressive Player - tend to capture as many as possible

## UI
![image](https://user-images.githubusercontent.com/89559531/165950259-f9ab7605-9a49-46da-83dd-1650809b0cb6.png)


### Contribution
We build our fundamental rules and create a random player together in the first stage. Then, Yawen mainly worked on UI and Candice developed the two Minimax players. 


### Reference
* GUI https://www.youtube.com/watch?v=vnd3RfeG3NM
* Minimax pseudocode  https://www.youtube.com/watch?v=l-hh51ncgDI&t=254s
