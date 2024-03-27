import numpy as np
import random


class Connect4:
    def __init__(self, h=6, w=7, k=4,playerCount = 2):
        self.h = h
        self.w = w
        self.k = k
        self.toMove = [-1, -1, -1, -1]
        self.players = []
        self.playerCount = playerCount
        self.state = 0
        self.board = np.zeros((h, w))

    def getState():
        return self.state

    def getBoardString(self):
        return np.array2string(self.board)

    # returns all legal moves
    def legalMoves(self):
        moves = []
        for i in range(self.w):
            if self.board[0][i] == 0:
                moves.append(i)
        return moves

    # returns true if draw false others
    def checkForDraw(self):
        if self.checkForWin() is False and len(self.legalMoves()) == 0:
            return True
        return False

    # returns true if placing a tile was successful
    def placeTile(self, row):
        if int(row) not in self.legalMoves():
            raise Exception("Not a legal move")
        for i in range(self.h):
            if self.board[self.h - 1 - i][row] == 0:
                self.board[self.h - 1 - i][row] = self.toMove[0]
                return True
        return False

    # returns true if there are any k connected tiles on the board otherwise returns false
    def checkForWin(self):
        for c in range(self.w - 3):
            for r in range(self.h):
                if self.board[r][c] == self.toMove[0] and self.board[r][
                    c + 1] == self.toMove[0] and self.board[r][
                    c + 2] == self.toMove[0] and self.board[r][
                    c + 3] == self.toMove[0]:
                    return True
        for c in range(self.w):
            for r in range(self.h - 3):
                if self.board[r][c] == self.toMove[0] and self.board[r + 1][
                    c] == self.toMove[0] and self.board[r + 2][
                    c] == self.toMove[0] and self.board[r + 3][
                    c] == self.toMove[0]:
                    return True
        for c in range(self.w - 3):
            for r in range(self.h - 3):
                if self.board[r][c] == self.toMove[0] and self.board[r + 1][
                    c + 1] == self.toMove[0] and self.board[r + 2][
                    c + 2] == self.toMove[0] and self.board[r + 3][
                    c + 3] == self.toMove[0]:
                    return True
        for c in range(self.w - 3):
            for r in range(3, self.h):
                if self.board[r][c] == self.toMove[0] and self.board[r - 1][
                    c + 1] == self.toMove[0] and self.board[r - 2][
                    c + 2] == self.toMove[0] and self.board[r - 3][
                    c + 3] == self.toMove[0]:
                    return True
        return False

    def addPlayer(self, requestid,id,token):
        playerNumber = len(self.players)
        self.players.append([playerNumber + 1, requestid, id,token])
        if len(self.players) == self.playerCount:
            self.changeState()
            return
        print(self.players)

    def changeToMove(self):
        toMoveIndex = self.players.index(self.toMove) + 1
        if(toMoveIndex == len(self.players)):
            toMoveIndex = 0
        self.toMove = self.players[toMoveIndex]

    def changeState(self):
        if self.state == 0:
            self.state = 1
            self.toMove = random.choice(self.players)
            return
        if self.state == 1:
            self.state = 0
            self.__init__()
            self.toMove = (-1, -1)
            return
