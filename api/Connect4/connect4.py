import numpy as np
import random


class Connect4:
    """Play TicTacToe on a h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=6, w=7, k=3):
        self.h = h
        self.w = w
        self.k = k
        self.toMove = [(-1, -1)]
        self.players = []
        self.state = 0
        self.board = np.zeros((h, w))

    def getBoard(self):
        return self.board

    # returns all legal moves
    def legalMoves(self):
        moves = 0
        for i in range(self.w):
            for j in range(self.h):
                if self.board == 0:
                    moves += 1
                    break
        return moves

    # returns true if draw false others
    def drawCheck(self):
        if self.checkForWin() is False and self.legalMoves() == 0:
            return True
        return False

    # returns true if placing a tile was successful
    def placeTile(self, row):
        for i in range(self.h):
            if self.board[self.h - 1 - i][row] == 0:
                self.board[self.h - 1 - i][row] = self.toMove[0]
                return True
        return False

    # returns true if there are any k connected tiles on the board otherwise returns false
    def checkForWin(self):
        for c in range(self.h - 3):
            for r in range(self.w):
                if self.board[r][c] == self.toMove[0] and self.board[r][
                    c + 1] == self.toMove[0] and self.board[r][
                    c + 2] == self.toMove[0] and self.board[r][
                    c + 3] == self.toMove[0]:
                    return True
        for c in range(self.h):
            for r in range(self.w - 3):
                if self.board[r][c] == self.toMove[0] and self.board[r + 1][
                    c] == self.toMove[0] and self.board[r + 2][
                    c] == self.toMove[0] and self.board[r + 3][
                    c] == self.toMove[0]:
                    return True
        for c in range(self.h - 3):
            for r in range(self.w - 3):
                if self.board[r][c] == self.toMove[0] and self.board[r + 1][
                    c + 1] == self.toMove[0] and self.board[r + 2][
                    c + 2] == self.toMove[0] and self.board[r + 3][
                    c + 3] == self.toMove[0]:
                    return True
        for c in range(self.h - 3):
            for r in range(3, self.w):
                if self.board[r][c] == self.toMove[0] and self.board[r - 1][
                    c + 1] == self.toMove[0] and self.board[r - 2][
                    c + 2] == self.toMove[0] and self.board[r - 3][
                    c + 3] == self.toMove[0]:
                    return True
        return False

    def addPlayer(self, id):
        playerNumber = len(self.players)
        self.players.append((playerNumber + 1, id))
        if len(self.players) == 2:
            return

    def changeState(self):
        if self.state == 0:
            self.state = 1
            self.toMove = random.choice(self.players)
            return
        if self.state == 1:
            self.state = 2
            self.toMove = None
            return
