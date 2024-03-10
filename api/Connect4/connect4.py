import numpy as np
import random


class Connect4():
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=6, w=7, k=3):
        self.h = h
        self.w = w
        self.k = k
        self.moves = []
        self.toMove = [(-1,-1)]
        self.players = []
        self.state = 0
        self.board = np.zeros((h, w))

    def getBoard(self):
        raise NotImplementedError
    # returns all legal moves
    def legalMoves(self):
        raise NotImplementedError

    # returns true if draw false others
    def drawCheck(self):
        raise NotImplementedError

    # returns true if placing a tile was successful
    def placeTile(self):
        raise NotImplementedError

    # returns true if there are any k connected tiles on the board otherwise returns false
    def checkForWin(self):
        raise NotImplementedError

    def addPlayer(self,id):
        playerNumber = len(self.players)
        self.players.append((playerNumber+1,id))
        if(len(self.players) == 2):
            return

    def changeState(self):
        if(self.state == 0):
            self.state = 1
            self.toMove = random.choice(self.players)
            return
        if(self.state == 1):
            self.state = 2
            self.toMove = None
            return
