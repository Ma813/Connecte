import random
import copy
import numpy as np
from Connect4.connect4 import Connect4
import time
class AiPlayer:

    def __init__(self,depth):
        self.depth = depth


    def CalculateMove(self,game):
        start = time.time()
        values = []
        board = copy.deepcopy(game.board)
        player = game.toMove[0]
        for x in self.legalMoves(board):
            tempBoard = board.copy()
            tempBoard = self.placeTile(tempBoard,x,player)
            value = self.AlphabetPruning(tempBoard,self.depth,float("-inf"),float("inf"),player,player)
            values.append([x,value])
        maxMove = -1
        maxValue = float("-inf")
        random.shuffle(values)
        print(values)
        for i in range(0,len(values)):
            if(values[i][1] > maxValue):
                maxMove = values[i][0]
                maxValue = values[i][1]
        end = time.time()
        print("time taken:",end - start,"seconds")
        return maxMove
            
    def setUpGame(self,toMove,board):
        game = Connect4()
        game.board = np.copy(board)
        game.players.append([1, 0, 0,0,""])
        game.players.append([2, 0, 0,0,""])
        game.state = 1
        game.toMove = [toMove, 0, 0,0,""]    
        return game    

    def AlphabetPruning(self,board,depth,a,b,player,originalPlayer):
        
        if(self.checkForWin(board,player)):
            return 1 if player == originalPlayer else -1
        if depth == 0 or self.checkForDraw(board):
            return 0

        if(player == 1):
            player = 2
        else:
            player = 1

        if player == originalPlayer:
            value = float("-inf")
            for x in self.legalMoves(board):
                tempBoard = board.copy()
                tempBoard = self.placeTile(tempBoard,x,player)
                value = max(value, self.AlphabetPruning(tempBoard,depth-1,a,b,player,originalPlayer))
                if value >= b:
                    break;
                a = max(a,value)
            return value
        else:
            value = float("inf")
            for x in self.legalMoves(board):
                tempBoard = board.copy()
                tempBoard = self.placeTile(tempBoard,x,player)
                value = min(value, self.AlphabetPruning(tempBoard,depth-1,a,b,player,originalPlayer))
                if value <= a:
                    break;
                b = min(b,value)
            return value
            
    def checkForDraw(self,board):
        if len(self.legalMoves(board)) == 0:
            return True
        return False

    def legalMoves(self,board):
        moves = []
        for i in range(7):
            if board[0][i] == 0:
                moves.append(i)
        return moves

    def placeTile(self, board,row,player):
        for i in range(6):
            if board[6 - 1 - i][row] == 0:
                board[6 - 1 - i][row] = player
                return board
        
    
    def checkForWin(self,board,color):
        h = 6
        w = 7
        # Check horizontal locations for win
        for c in range(w-3):
            for r in range(h):
                if board[r][c] == color and board[r][c+1] == color and board[r][c+2] == color and board[r][c+3] == color:
                    return True

        # Check vertical locations for win
        for c in range(w):
            for r in range(h-3):
                if board[r][c] == color and board[r+1][c] == color and board[r+2][c] == color and board[r+3][c] == color:
                    return True

        # Check positively sloped diaganols
        for c in range(w-3):
            for r in range(h-3):
                if board[r][c] == color and board[r+1][c+1] == color and board[r+2][c+2] == color and board[r+3][c+3] == color:
                    return True

        # Check negatively sloped diaganols
        for c in range(w-3):
            for r in range(3, h):
                if board[r][c] == color and board[r-1][c+1] == color and board[r-2][c+2] == color and board[r-3][c+3] == color:
                    return True
        return False