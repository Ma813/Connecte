import numpy as np
import random


class Connect4:
    def __init__(self, h=6, w=7, k=4, playerCount=2, gameMode = 1):
        self.h = h
        self.w = w
        self.k = k
        self.toMove = [-1, -1, -1, -1, "name"] # color, requestID, cookie, token, username
        self.players = []
        self.playerCount = playerCount
        self.state = 0
        self.board = np.zeros((h, w))
        self.gameMode = gameMode

    def getState(self):
        return self.state

    def changeMode(self):
        self.mode = 1

    def getBoardString(self):
        if self.gameMode == 1:
            return np.array2string(self.board)
        else:
            return np.array2string(self.singleColor())

    def singleColor(self):
        newBoard = np.zeros((self.h, self.w))
        for x in range (0, self.h):
            for y in range (0, self.w):
                if self.board[x][y] != 0:
                    newBoard[x][y] = 5

        return newBoard
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

    # returns true if there are any k connected tiles on the board otherwise returns false
    def checkForWin(self):
        color = self.toMove[0]
        for c in range(self.w - self.k + 1):
            for r in range(self.h):
                for i in range(self.k):
                    if self.board[r][c + i] != color:
                        break
                    if i == self.k - 1:
                        return True
                    
        for c in range(self.w):
            for r in range(self.h - self.k + 1):
                for i in range(self.k):
                    if self.board[r + i][c] != color:
                        break
                    if i == self.k - 1:
                        return True
        
        for c in range(self.w - self.k + 1):
            for r in range(self.h - self.k + 1):
                for i in range(self.k):
                    if self.board[r + i][c + i] != color:
                        break
                    if i == self.k - 1:
                        return True
                    
        for c in range(self.w - self.k + 1):
            for r in range(self.k - 1, self.h):
                for i in range(self.k):
                    if self.board[r - i][c + i] != color:
                        break
                    if i == self.k - 1:
                        return True
        return False

    def addPlayer(self, requestid,id,token,name):
        playerNumber = len(self.players)
        self.players.append([playerNumber + 1, requestid, id,token,name])

        if len(self.players) == self.playerCount:
            self.changeState()
            return
    

    def changeToMove(self):
        toMoveIndex = self.players.index(self.toMove) + 1
        if (toMoveIndex == len(self.players)):
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
