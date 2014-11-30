"""
Taylor Martin
mail@tmrt.in (tm40@indiana.edu)

a Monte Carlo Backgammon AI


The MIT License (MIT)

Copyright (c) 2014 Taylor Martin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import random

class Board:
    def __init__(self, p1vec, p2vec):
        self.p1vec = p1vec[:]
        self.p2vec = p2vec[:]

    def __str__(self):
        s = ""
        for i in range(13,25):
            if (self.p1vec[i] > 0):
                s += "|W{0:02}|".format(self.p1vec[i])
            elif (self.p2vec[25 - i] > 0):
                s += "|B{0:02}|".format(self.p2vec[25 - i])
            else:
                s += "|   |"
        s += '\n'
        for i in range(12, 0,-1):
            if (self.p1vec[i] > 0):
                s += "|W{0:02}|".format(self.p1vec[i])
            elif (self.p2vec[25 - i] > 0):
                s += "|B{0:02}|".format(self.p2vec[25 - i])
            else:
                s += "|   |"
        return s
        

    def move(self, start, distance, p1):
        if (p1):
            #move your piece
            self.p1vec[start] -= 1
            self.p1vec[start+distance] += 1
            
            #capture you opponent
            spot = 25 - start - distance
            self.p2vec[0] += self.p2vec[spot]
            self.p2vec[spot] = 0
        else:
            #move your piece
            self.p2vec[start] -= 1
            self.p2vec[start+distance] += 1
            
            #capture you opponent
            spot = 25 - start - distance
            self.p2vec[0] += self.p2vec[spot]
            self.p2vec[spot] = 0
            
    def find_moveable_pieces(self, die, p1):
        """finds moveable pieces given the player, opp,
            and one die"""            
        moveable = []
        if (p1):
            #must we re-enter?
            if (self.p1vec[0] > 0):
                if (self.free_spot(0, die, p1)):
                    b = Board(self.p1vec[:],self.p2vec[:])
                    b.move(0, die, p1)
                    moveable.append(b)
            #no? ok then generate the moves
            else:
                for i in range(1, 24):
                    if (self.p1vec[i] > 0):
                        if (self.free_spot(i, die, p1)):
                            b = Board(self.p1vec[:],self.p2vec[:])
                            b.move(0, die, p1)
                            moveable.append(b)
        else:
            #must we re-enter?
            if (self.p2vec[0] > 0):
                if (free_spot(0, die, p1)):
                    b = Board(self.p1vec[:],self.p2vec[:])
                    b.move(0, die, p1)
                    moveable.append(b)
            #no? ok then generate the moves
            else:
                for i in range(1, 24):
                    if (self.p2vec[i] > 0):
                        if (self.free_spot(i, die, p1)):
                            b = Board(self.p1vec[:],self.p2vec[:])
                            b.move(0, die, p1)
                            moveable.append(b)
        
        print(moveable)    
        return moveable
                            

    def free_spot(self, start, distance, p1):
        """returns true if spot can be captured or is free"""
        free = False
        spot = 25 - start - distance
        #do we have a valid position to consider?
        if (spot > 0):
            #which player are we?
            if (p1):
                if (self.p2vec[spot] < 2):
                    free = True
            else:
                if (self.p1vec[spot] < 2):
                    free = True
        if (spot == 0):
            free = True
        return free

class Game:
    """A class to model a gameboard, provide valid moves,
    roll dice, play to completion"""
    

    """Sets up the board with two player state vectors,
    0 is for captured pieces and 1:24 for number of pieces,
    on each spot"""
    def __init__(self, board):
        self.p1ply = True
        self.roll = (0,0)
        #array of applied board states
        self.moves = []
        self.board = board
    
    """Simple function to set the current roll to a tuple of
    1..6 inclusive int"""
    def roll_dice(self):
        self.roll = (random.randint(1,6), random.randint(1,6))
        return self.roll
    
    """function that uses the current roll state and ply bool
    to generate a list of all valid moves, considers barred
    pieces"""
    def generate_valid_moves(self, player):                
        #make sure we have a valid roll
        if (self.roll != (0,0)):
            
            #if doubles, need to do 4 moves
            #if (self.roll[0] == self.roll[1]):
            #    pass
            #else:
                #find moveset, d1 then d2, and d2 then d1
                d1d2 = self.board.find_moveable_pieces(self.roll[0], player)
                d2d1 = self.board.find_moveable_pieces(self.roll[1], player)
        return random.choice(d1d2)
            
            
                
            
            
def main():
    g = Game(Board([0,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                   [0,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    g.roll_dice()
    print(g.generate_valid_moves(False))

if __name__ == "__main__":
    main()
