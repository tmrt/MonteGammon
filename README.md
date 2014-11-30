MonteGammon
===========

a Monte Carlo backgammon AI 


##TODO

1. Represent Board/Game state
  1. ~~Player vectors, list howmany pieces are on each spot for each player~~
  2. ~~Which turn~~
  3. ~~Moves~~
  4. ~~last roll~~
  5. Printing
2. Generate valid moves
  1. Moves are applied to boards, to make applied board states.
  2. consider pieces on bar waiting to re-enter 
  3. ~~should double moveable pieces for doubles~~
3. ~~Roll Die~~
4. Randomly select valid move
  1. Always select for bearoff
  2. Protect lone piece
  3. Capture lone piece
5. Rollout for all valid moves at first level (2-4 until completion)
6. Compare branches for best move
7. PDF Presentation
8. Multithreaded
