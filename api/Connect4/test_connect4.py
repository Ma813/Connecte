import numpy as np
from numpy import array
from connect4 import Connect4
import pytest

#pip install pytest
#pip install pytest-cov
#pip install coverage
#pytest --cov-report term-missing --cov=connect4

@pytest.fixture
def game_empty():
    game = Connect4(6, 7, 4, 4)
    game.players = []
    game.state = 0
    game.board = np.zeros((game.h, game.w), dtype=int)
    game.toMove = [-1, -1, -1, -1]
    
    return game

#Game in progress, just started
@pytest.fixture
def game_start():
    game = Connect4(3, 4, 3, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", None], #player 2 is no logged in
    ]

    game.state = 1
    game.board = np.zeros((game.h, game.w), dtype=int)
    game.toMove = game.players[0]
    
    return game
    
#Only one player has joined
@pytest.fixture
def game_one_player():
    game = Connect4(6, 7, 4, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
    ]

    game.state = 0
    game.board = np.zeros((game.h, game.w), dtype=int)
    
    game.toMove = [-1, -1, -1, -1]
    
    return game

@pytest.fixture
def game_in_progress():
    game = Connect4(4, 4, 3, 3)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"],
        [3, "req3", "cookie3", None]]
    game.state = 1
    game.board = array([[1, 0, 0, 0],
                    [2, 0, 0, 0,], 
                    [3, 0, 0, 2],
                    [1, 0, 0, 1]])
    
    game.toMove = game.players[2]
    
    return game

@pytest.fixture
def game_drawn():
    game = Connect4(3, 3, 3, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"]]
    game.state = 1
    game.board = array([[1, 2, 1], [2, 1, 2], [2, 1, 2]])
    game.toMove = game.players[0]
    
    return game

@pytest.fixture
def game_won_vertical():
    game = Connect4(4, 4, 3, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"]]
    game.state = 1
    game.board = array([[2, 0, 0, 0],
                        [2, 2, 0, 2],
                        [1, 1, 1, 2],
                        [1, 1, 2, 1]])
    game.toMove = game.players[0]

    return game

@pytest.fixture
def game_won_horizontal():
    game = Connect4(3, 3, 2, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"]]
    game.state = 1
    game.board = array([[0, 0, 0],
                        [1, 0, 0],
                        [1, 2, 0]])
    game.toMove = game.players[0]
    
    return game
    
@pytest.fixture
def game_won_diagonal():
    game = Connect4(3, 3, 3, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"]]
    game.state = 1
    game.board = array([[0, 0, 2],
                        [1, 2, 0],
                        [2, 1, 1]])
    game.toMove = game.players[1]
    
    return game

@pytest.fixture
def game_won_diagonal2():
    game = Connect4(3, 3, 3, 2)
    game.players = [
        [1, "req1", "cookie1", "token1"],
        [2, "req2", "cookie2", "token2"]]
    game.state = 1
    game.board = array([[2, 0, 1],
                        [1, 2, 0],
                        [1, 1, 2]])
    game.toMove = game.players[1]
    
    return game

@pytest.mark.parametrize('game, expected',
    [('game_start', 1),
    ('game_one_player', 0)])
def test_getState(game, expected, request):
    result = request.getfixturevalue(game).getState()
    assert result == expected
    
@pytest.mark.parametrize('game, expected',
    [('game_start', "[[0 0 0 0]\n [0 0 0 0]\n [0 0 0 0]]"),
    ('game_one_player', "[[0 0 0 0 0 0 0]\n [0 0 0 0 0 0 0]\n [0 0 0 0 0 0 0]\n [0 0 0 0 0 0 0]\n [0 0 0 0 0 0 0]\n [0 0 0 0 0 0 0]]"),
    ('game_in_progress', "[[1 0 0 0]\n [2 0 0 0]\n [3 0 0 2]\n [1 0 0 1]]"),
    ('game_drawn', "[[1 2 1]\n [2 1 2]\n [2 1 2]]")])
def test_getBoardString(game, expected, request):
    result = request.getfixturevalue(game).getBoardString()
    assert result == expected
    
@pytest.mark.parametrize('game, expected',
    [('game_start', [0, 1, 2, 3]),
    ('game_one_player', [0, 1, 2, 3, 4, 5, 6]),
    ('game_in_progress', [1, 2, 3]),
    ('game_drawn', [])])
def test_legalMoves(game, expected, request):
    result = request.getfixturevalue(game).legalMoves()
    assert result == expected

@pytest.mark.parametrize('game, expected',
    [('game_start', False),
    ('game_one_player', False),
    ('game_in_progress', False),
    ('game_drawn', True),
    ('game_won_vertical', False)])
def test_checkForDraw(game, expected, request):
    result = request.getfixturevalue(game).checkForDraw()
    assert result == expected

@pytest.mark.parametrize('game, expected',
    [('game_start', False),
    ('game_one_player', False),
    ('game_in_progress', False),
    ('game_drawn', False),
    ('game_won_vertical', True),
    ('game_won_horizontal', True),
    ('game_won_diagonal', True),
    ('game_won_diagonal2', True)])
def test_checkForWin(game, expected, request):
    result = request.getfixturevalue(game).checkForWin()
    assert result == expected
    
def test_addPlayer_startsGame(game_one_player):
    game = game_one_player
    game.addPlayer("req2", "cookie2", "token2")
    assert game.state == 1 and len(game.players) == 2
    
def test_addPlayer_doesNotStartGame(game_empty):
    game = game_empty
    game.addPlayer("req2", "cookie2", "token2")
    assert game.state == 0 and len(game.players) == 1
    
@pytest.mark.parametrize('game, expected',[
    ('game_in_progress', 0),
    ('game_start', 1)])
def test_changeToMove(game, expected, request):
    game = request.getfixturevalue(game)
    game.changeToMove()
    assert game.toMove == game.players[expected]
    
def test_placeTile_Illegal(game_in_progress):
    game = game_in_progress
    pytest.raises(Exception, game.placeTile, 0)
    
def test_placeTile_Legal(game_in_progress):
    game = game_in_progress
    game.placeTile(1)
    assert game.board[3][1] == 3
    
def test_changeState_EndingGame(game_drawn):
    game = game_drawn
    game.changeState()
    assert game.state == 0
