"""
Taylor Martin
mail@tmrt.in (tm40@indiana.edu)

a Monte Carlo Backgammon AI


The MIT License (MIT)

Copyright (c) 2014 Taylor Martin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
>to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
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
import multiprocessing as mp

class Board:
    """This models the board state as 2 vectors. It provides movement and 
    capturing mechanisms. Provides basic checks on move legality, and finds
    pieces that can be moved."""
    def __init__(self, p1vec, p2vec):
        self.p1vec = p1vec[:]
        self.p2vec = p2vec[:]
        self.bornoff = False
        
    def __hash__(self):
        return hash(reduce(lambda x, y: 10 * x + y, self.p1vec + self.p2vec))
 
    def __eq__(self, other):
        return (self.p1vec == other.p1vec) and (self.p2vec == other.p2vec)

    def __str__(self):
        """Builds a string representation of the board."""
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
        """Given a starting piece and a distance to travel, this moves
        a piece to the new spot. It performs captures, but does not check
        for legality. In the event of illegal moves, tries to keep playable
        board state"""
        if (p1):
            #move your piece
            self.p1vec[start] -= 1
            dest = start + distance
            if (dest == 25):
                self.bornoff = True
            else:
                self.p1vec[start+distance] += 1
                #capture your opponent, despite their number
                spot = 25 - start - distance
                self.p2vec[0] += self.p2vec[spot]
                self.p2vec[spot] = 0
        else:
            #move your piece
            self.p2vec[start] -= 1
            dest = start + distance
            if (dest == 25):
                pass
            else:
                self.p2vec[start+distance] += 1
                #capture your opponent
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
                for i in range(1, 25):
                    if (self.p1vec[i] > 0):
                        if (self.free_spot(i, die, p1)):
                            b = Board(self.p1vec[:],self.p2vec[:])
                            b.move(i, die, p1)
                            moveable.append(b)
        else:
            #must we re-enter?
            if (self.p2vec[0] > 0):
                if (self.free_spot(0, die, p1)):
                    b = Board(self.p1vec[:],self.p2vec[:])
                    b.move(0, die, p1)
                    moveable.append(b)
            #no? ok then generate the moves
            else:
                for i in range(1, 25):
                    if (self.p2vec[i] > 0):
                        if (self.free_spot(i, die, p1)):
                            b = Board(self.p1vec[:],self.p2vec[:])
                            b.move(i, die, p1)
                            moveable.append(b)
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
    
    def __init__(self, board, turn):
        """Sets up the board with two player state vectors,
        0 is for barred pieces and 1:24 for number of pieces,
        on each spot. Starts off with player 1 as playing, rolls the dice
        and finds valid moves."""
        self.player = turn
        self.roll = self.roll_dice()
        #array of applied board states
        self.moves = []
        self.board = board
        self.generate_valid_moves()
    
    def __str__(self):
        return self.board.__str__()
    
    def roll_dice(self):
        """Simple function to set the current roll to a tuple of
        1..6 inclusive int"""
        self.roll = (random.randint(1,6), random.randint(1,6))
        return self.roll
    
    def generate_valid_moves(self):                
        """function that uses the current roll state and ply bool
        to generate a list of all valid moves applied to a boar, considers 
        barred pieces through find_moveable_pieces, performs doubles"""
        #make sure we have a valid roll
        if (self.roll != (0,0)):
            #if doubles, need to do 4 moves
            if (self.roll[0] == self.roll[1]):
                #need to seed the initial moveset
                mv = self.board.find_moveable_pieces(self.roll[0], self.player)
                mv2 = []
                #apply the remaining 3 rolls
                for i in range(0,3):
                    for mboard in mv:
                        mv2.extend(mboard.find_moveable_pieces(self.roll[0], self.player))
                    mv = list(set(mv2))
                    mv2 = []
            else:
                #need to condisider d1 then d2 and d2 then d1
                d1d2 = self.board.find_moveable_pieces(self.roll[0], self.player)
                d2d1 = self.board.find_moveable_pieces(self.roll[1], self.player)
                d1d2_2 = []
                d2d1_2 = []
                for mboard in d1d2:
                    d1d2_2.extend(mboard.find_moveable_pieces(self.roll[1], self.player))
                for mboard in d2d1:
                    d2d1_2.extend(mboard.find_moveable_pieces(self.roll[0], self.player))
                mv = d1d2_2
                mv.extend(d2d1_2)
            self.moves = list(set(mv))

    def select_move(self):
        """Returns a move from the possible moves. Favors, in order:
        1) Bearoff
        2) Lone piece Protection
        3) Capture piece
        4) Random"""
        move = None
        bearoff = True
        lone = True
        capture = True
        for m in self.moves:
            if (m.bornoff and bearoff):
                move = m
                bearoff = False
            elif ((.5 < random.random()) and bearoff and lone):
                if (self.protect_lone(m)):
                    move = m
                    lone = False
                elif ((.5 < random.random()) and self.find_lone(m) and capture):
                    move = m
                    capture = False
        #if no move bearsoff, protects a lone, or captures, do something random
        if (bearoff and lone and capture):
            move = random.choice(self.moves)
        move.bornoff = False
        return move

    def bornoff(self, board):
        """Detects if a piece has been bornoff by comparing the vector sums"""
        res = False
        if (self.player):
            if (reduce(lambda x, y: x+y, board.p1vec) < reduce(lambda x, y: x+y, self.board.p1vec)):
                res = True
        else:
            if (reduce(lambda x, y: x+y, board.p2vec) < reduce(lambda x, y: x+y, self.board.p2vec)):
                res = True
        return res

    def protect_lone(self, board):
        """Detects if the number of lone pieces in decreased"""
        res = False
        if (self.player):
            if (reduce(lambda x, y: x if (y > 1) else x + 1, board.p1vec) < \
                reduce(lambda x, y: x if (y > 1) else x + 1, self.board.p1vec)):
                res = True
        else:
            if (reduce(lambda x, y: x if (y > 1) else x + 1, board.p2vec) < \
                reduce(lambda x, y: x if (y > 1) else x + 1, self.board.p2vec)):
                res = True
        return res

    def find_lone(self, board):
        """Detects if a captured happened in a move"""
        res = False
        if (self.player):
            if (self.board.p2vec[0] > board.p2vec[0]):
                res = True
        else:
            if (self.board.p1vec[0] > board.p1vec[0]):
                res = True
        return res

    def winner(self):
        """Determines if there is a winner by checking if there are any pieces
        left to remove. (sums the player vector and looks for 0)"""
        if (self.player):
            return (0 == reduce(lambda x, y: x+y, self.board.p1vec))
        else:
            return (0 == reduce(lambda x, y: x+y, self.board.p2vec))
    
    def next_turn(self):
        """This selects a new board state, flips the turn, rolls dice""" 
        if (self.moves):
            self.board = self.select_move() 
        self.moves = []
        self.roll = self.roll_dice()
        self.player = not self.player
        self.generate_valid_moves()
 
class MonteRunner:
    """Takes a Game with a Board state, looks at its possible moves, and runs a
    Monte Carlo Simulation on each of the moves"""
    def __init__(self):
        #set up a new board
        self.g = Game(Board([0,6,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,6,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), True)
        self.branches = self.g.moves
     
    def find_best_move(self):
        q = mp.Queue()
        procs = [mp.Process(target=self.task, args=(x,q,)) for x in self.branches]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        results = []
        while not q.empty():
            results.append(q.get())
        results.sort(key=lambda r: -1 * r[1])
        for r in results:
            print("Move:--------------------------------------------------")
            print("{} has score: {}".format(r[0].__str__(), r[1]))
        
    def task(self, branch, q):
        win = 0
        loss = 0
        draw = 0
        trials = 50
        for i in range (1, trials):
            simGame = Game(Board(branch.p1vec, branch.p2vec), False)
            i = 1
            steps = 300
            while (not simGame.winner() and i < steps):
                simGame.next_turn()
                #print(g)
                i += 1
            if (i < steps):
                if (simGame.player):
                    win += 1
                else:
                    loss += 1
            else:
                draw += 1
        q.put((branch,(win + .3 * draw)/(1.0 * trials)))

def main():
    m = MonteRunner()
    print("Starting from this position and roll: {}".format(m.g.roll))
    print("{}\n---------------------------------------".format(m.g.board.__str__()))
    m.find_best_move()
       
if __name__ == "__main__":
    main()
