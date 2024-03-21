import unittest
import numpy as np
from connect4 import Connect4

class Connect4Tests(unittest.TestCase):

    def setUp(self):
        self.game = Connect4()

    def test_getState(self):
        self.assertEqual(self.game.getState(), 0)

    def test_getBoardString(self):
        expected_board = np.zeros((6, 7))
        self.assertEqual(self.game.getBoardString(), np.array2string(expected_board))

    def test_legalMoves(self):
        expected_moves = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(self.game.legalMoves(), expected_moves)

    def test_checkForDraw(self):
        self.assertFalse(self.game.checkForDraw())

    def test_placeTile(self):
        self.assertTrue(self.game.placeTile(0))
        self.assertEqual(self.game.getBoardString(), np.array2string(np.array([
            [-1.,  0.,  0.,  0.,  0.,  0.,  0.],
            [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
            [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
            [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
            [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
            [ 0.,  0.,  0.,  0.,  0.,  0.,  0.]]
        )))

    def test_checkForWin(self):
        self.assertFalse(self.game.checkForWin())

    def test_addPlayer(self):
        self.game.addPlayer(1)
        self.assertEqual(len(self.game.players), 1)
        self.assertEqual(self.game.getState(), 1)

    def test_changeToMove(self):
        self.game.addPlayer(1)
        self.game.addPlayer(2)
        self.game.changeToMove()
        self.assertEqual(self.game.toMove, (2, 2))

    def test_changeState(self):
        self.game.changeState()
        self.assertEqual(self.game.getState(), 1)
        self.assertEqual(self.game.toMove, (-1, -1))

if __name__ == '__main__':
    unittest.main()