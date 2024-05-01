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
        for x in game.legalMoves():
            tempGame = self.setUpGame(game.toMove[0],game.board)
            tempGame.placeTile(x)
            value = self.AlphabetPruning(tempGame,self.depth,float("-inf"),float("inf"),game.toMove[0])
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

    def AlphabetPruning(self,game,depth,a,b,player):
        if(game.checkForWin()):
            return 1 if player == game.toMove[0] else -1
        if depth == 0 or game.checkForDraw():
            return 0
        game.changeToMove()
        if game.toMove[0] == player:
            value = float("-inf")
            for x in game.legalMoves():
                tempGame = self.setUpGame(game.toMove[0],game.board)
                tempGame.placeTile(x)
                value = max(value, self.AlphabetPruning(tempGame,depth-1,a,b,player))
                if value >= b:
                    break;
                a = max(a,value)
            return value
        else:
            value = float("inf")
            for x in game.legalMoves():
                tempGame = self.setUpGame(game.toMove[0],game.board)
                tempGame.placeTile(x)
                value = min(value, self.AlphabetPruning(tempGame,depth-1,a,b,player))
                if value <= a:
                    break;
                b = min(b,value)
            return value
    
            