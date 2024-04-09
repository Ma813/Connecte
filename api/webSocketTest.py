from unittest.mock import patch
from unittest import TestCase
import unittest
import json
from app import app
from extensions import socketio

class TestServerResource(TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client


    @patch('WebSocket.webSocket')
    def test_bad_url(self,mock):
        res = self.client().get('/bad')
        self.assertEqual(res.status_code, 404)

    @patch('WebSocket.webSocket.getRoom')
    def test_GetRoom(self, mock):
        res = self.client().get('/getRoom')
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.text)
        self.assertTrue("gameId" in response)
        self.assertTrue(response["gameId"].islower())
        self.assertEqual(len(response["gameId"]),8)

    def test_handleJoinNoData(self):
        clientSocketio = socketio.test_client(self.app)
        clientSocketio.emit('join','')
        received = clientSocketio.get_received()
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'error')
        self.assertEqual(received[0]['args'][0]['state'], 'no_room_found')

    def test_handleJoinFakeGameId(self):
        clientSocketio = socketio.test_client(self.app)
        clientSocketio.emit('join',{'gameId': 123})
        received = clientSocketio.get_received()
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'error')
        self.assertEqual(received[0]['args'][0]['state'], 'no_room_found')

    def test_handleJoinNoId(self):
        clientSocketio = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio.emit('join',{'gameId': response['gameId']})
        received = clientSocketio.get_received()
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'error')
        self.assertEqual(received[0]['args'][0]['state'], 'no_room_found')
    
    def test_handleJoinNoToken(self):
        clientSocketio = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio.emit('join',{'gameId': response['gameId'],'id':"123"})
        received = clientSocketio.get_received()
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'error')
        self.assertEqual(received[0]['args'][0]['state'], 'no_room_found')

    def test_handleJoinCorrect(self):
        clientSocketio = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio.emit('join',{'gameId': response['gameId'],'id':"123",'token':"123"})
        received = clientSocketio.get_received()
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'cookie')
        self.assertEqual(len(received[1]['args']), 1)
        self.assertEqual(received[1]['name'], 'message')
        self.assertEqual(received[1]['args']['state'], 'waiting_for_one_player')
    
    def test_handleJoinTwoPlayers(self):
        clientSocketio1 = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio1.emit('join',{'gameId': response['gameId'],'id':"123",'token':"123"})
        received = clientSocketio1.get_received()
        #cookie recieved
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'cookie')
        self.assertEqual(len(received[1]['args']), 1)
        #gameState updated to waiting for player
        self.assertEqual(received[1]['name'], 'message')
        self.assertEqual(received[1]['args']['state'], 'waiting_for_one_player')
        clientSocketio2 = socketio.test_client(self.app)
        clientSocketio2.emit('join',{'gameId': response['gameId'],'id':"123123",'token':"123123"})
        received = clientSocketio2.get_received()
        #cookie recieved
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'cookie')
        #gameState updated to waiting for player
        self.assertEqual(len(received[1]['args']), 1)
        self.assertEqual(received[1]['name'], 'message')
        self.assertEqual(received[1]['args']['state'], 'waiting_for_one_player')
        #gameState updated to playing game
        self.assertEqual(len(received[2]['args']), 4)
        self.assertEqual(received[2]['name'], 'message')
        self.assertEqual(received[2]['args']['state'], 'playing_game')

    def test_handleJoinThreePlayers(self):
        clientSocketio1 = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio1.emit('join',{'gameId': response['gameId'],'id':"123",'token':"123"})
        clientSocketio2 = socketio.test_client(self.app)
        clientSocketio2.emit('join',{'gameId': response['gameId'],'id':"123123",'token':"123123"})
        clientSocketio3 = socketio.test_client(self.app)
        clientSocketio3.emit('join',{'gameId': response['gameId'],'id':"123123123",'token':"123123123"})
        received = clientSocketio3.get_received()
        #only game state recieved, no cookie
        self.assertEqual(len(received[0]['args']), 4)
        self.assertEqual(received[0]['name'], 'message')
        self.assertEqual(received[0]['args']['state'], 'playing_game')

    def test_handleIncorrectMove(self):
        clientSocketio1 = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio1.emit('join',{'gameId': response['gameId'],'id':"123",'token':"123"})
        received = clientSocketio1.get_received()
        clientSocketio2 = socketio.test_client(self.app)
        clientSocketio2.emit('join',{'gameId': response['gameId'],'id':"123123",'token':"123123"})
        received = clientSocketio2.get_received()
        if len(received) == 4:
            received = clientSocketio2.get_received()
            clientSocketio2.emit('move',{'gameId': response['gameId'], 'move': -1})
            received = clientSocketio2.get_received()
        else:
            received = clientSocketio1.get_received()
            clientSocketio1.emit('move',{'gameId': response['gameId'], 'move': -1})
            received = clientSocketio1.get_received()
        
        self.assertEqual(len(received[0]['args']), 5)
        self.assertEqual(received[0]['name'], 'message')
        self.assertEqual(received[0]['args']['state'], 'playing_game')
        self.assertTrue('error' in received[0]['args'])


    def test_handleMoveCorrect(self):
        clientSocketio1 = socketio.test_client(self.app)
        res = self.client().get('/getRoom')
        response = json.loads(res.text)
        clientSocketio1.emit('join',{'gameId': response['gameId'],'id':"123",'token':"123"})
        received = clientSocketio1.get_received()
        clientSocketio2 = socketio.test_client(self.app)
        clientSocketio2.emit('join',{'gameId': response['gameId'],'id':"123123",'token':"123123"})
        received = clientSocketio2.get_received()
        if len(received) == 4:
            clientSocketio2.emit('move',{'gameId': response['gameId'], 'move': 1})
            received = clientSocketio2.get_received()
        else:
            clientSocketio1.emit('move',{'gameId': response['gameId'], 'move': 1})
            received = clientSocketio1.get_received()
        self.assertEqual(len(received[0]['args']), 4)
        self.assertEqual(received[0]['name'], 'message')
        self.assertEqual(received[0]['args']['state'], 'playing_game')

    
if __name__ == '__main__':
    unittest.main()