import random
class Gameboard:
    """A class to model a gameboard, provide valid moves,
    roll dice, play to completion"""
    p1ply = True
    roll = (0,0)

    """Sets up the board with two player state vectors,
    0 is for captured pieces and 1:24 for number of pieces,
    on each spot"""
    def __init__(self, p1vec, p2vec):
        self.p1vec = p1vec
        self.p2vec = p2vec
    
    """Simple function to set the current roll to a tuple of
    1..6 inclusive int"""
    def roll(self):
        roll = (random.randint(1,6), random.randint(1,6))
        return roll
    

def main():
    g = Gameboard([],[])
    print(g.roll())

if __name__ == "__main__":
    main()
