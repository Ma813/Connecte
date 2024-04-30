'''This file is responsible for the game logic'''
import random
import numpy as np


class Connect4:
    '''This class is responsible for storing information about a game'''
    def __init__(self, h=6, w=7, k=4, playerCount=2, gameMode=1):
        self.h = h
        self.w = w
        self.k = k

        self.toMove = {
            "color": -1,
            "requestID": -1,
            "cookie": -1,
            "token": -1,
            "username": "name"
        }


        self.players = []
        self.playerCount = playerCount
        self.state = 0
        self.board = np.zeros((h, w))
        self.gameMode = gameMode
        

    def getState(self):
        '''Get the state of the game'''
        return self.state

    def changeMode(self):
        '''Change the game mode to normal mode'''
        self.gameMode = 1

    def getBoardString(self):
        '''Get the game's board as a string'''
        if self.gameMode == 1:
            return np.array2string(self.board,separator=',')
        else:
            return np.array2string(self.singleColor(),separator=',')

    def singleColor(self):
        '''Get the game's board as a string with only one color for every token on the board'''
        newBoard = np.zeros((self.h, self.w))
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.board[x][y] != 0:
                    newBoard[x][y] = 5

        return newBoard

    def legalMoves(self):
        '''Returns a list of legal moves that can be made in the game'''
        moves = []
        for i in range(self.w):
            if self.board[0][i] == 0:
                moves.append(i)
        return moves

    def checkForDraw(self):
        '''Returns true if the game reached a draw condition, otherwise returns false'''
        if self.checkForWin() is False and len(self.legalMoves()) == 0:
            return True
        return False

    def placeTile(self, row):
        '''Returns true if placing a tile was successful, otherwise raises an exception'''
        if int(row) not in self.legalMoves():
            raise Exception("Not a legal move")
        for i in range(self.h):
            if self.board[self.h - 1 - i][row] == 0:
                self.board[self.h - 1 - i][row] = self.toMove["color"]
                return True

    def checkForWin(self):
        '''Returns true if a player has won the game
        by connecting k tokens in a row, otherwise returns false'''
        color = self.toMove["color"]

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

    def addPlayer(self, requestid, id, token, name):
        '''Add a player to the game,
        if the player count is reached, change the game state to 1 (playing)'''
        playerNumber = len(self.players)

        self.players.append({
            "color": playerNumber + 1,
            "requestID": requestid,
            "cookie": id,
            "token": token,
            "username": name
            })

        if len(self.players) == self.playerCount:
            self.changeState()
            return

    def changeToMove(self):
        '''Change the player that is to move next'''
        toMoveIndex = self.players.index(self.toMove) + 1
        if toMoveIndex == len(self.players):
            toMoveIndex = 0
        self.toMove = self.players[toMoveIndex]

    def changeState(self):
        '''Change the game state to playing or reset the game if the game is over'''
        if self.state == 0:
            self.state = 1
            self.toMove = random.choice(self.players)
            return
        if self.state == 1:
            self.state = 0
            self.__init__()
            self.toMove = (-1, -1)
            return
