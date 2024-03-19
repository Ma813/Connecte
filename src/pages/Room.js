import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, createBrowserRouter } from 'react-router-dom';
import io from 'socket.io-client';
import '../styles/Default.css'
import '../styles/Connect4Board.css'
import GameEnd from './Game/GameEnd';
import DrawBoard from './Game/DrawBoard'


const Room = () => {
  const { gameId } = useParams();
  const [socket, setSocket] = useState(null);
  const [boardString, setBoard] = useState(null);
  const [move, setMove] = useState(null);
  const [error, setError] = useState(null);
  const [win, setWin] = useState(false)
  const [draw, setDraw] = useState(false);
  const [gameState, setGameState] = useState('loading');
  const [color, setColor] = useState(null);
  const navigate = useNavigate();

  let board = new Array(6).fill(null)
  .map(i => new Array(7).fill(null));

  const fullURL = window.location.href;

  useEffect(() => {

    // Establish a WebSocket connection to the server
    const newSocket = io(window.location.hostname + ':5000');
    setSocket(newSocket);

    newSocket.on('connect', () => {
      
      newSocket.emit('join', { 'gameId': gameId });
      
    });
    

    newSocket.on('message', (data) => {
      const state = data['state'];
      
      if (state == 'playing_game') {
        setBoard(data['board']);
        setMove(data['move']);
        setColor(data['color'])
        if ('error' in data) {
          setError(data['error'])
        }
        else {
          setError(null)
        }
      }
      if (state == 'game_end') {
        setBoard(data['board']);
        setMove(data['move']);
        setWin(data['winner'])
        setDraw(data['draw'])
        if ('error' in data) {
          setError(data['error'])
        }
        else {
          setError(null)
        }
      }


      setGameState(state);

    });
    
    return () => {

      
      newSocket.disconnect();
    };
  }, [gameId]);



  const renderWaitingForOnePlayer = () => (
    <div>
      <p className='message'>Waiting for one more player to join...</p>
      <p className='message'>Room ID is: <b>{gameId}</b></p>
      <p className='message'>Invite players with this URL: <b>{fullURL}</b> </p>
      <button className='copyButton' onClick={copyURL}>Copy URL</button>
      <button className='copyButton' onClick={copyID}>Copy Room ID</button>
    </div>

  );

 

  const copyURL = () => {
    navigator.clipboard.writeText(fullURL)
  }
  const copyID = () => {
    navigator.clipboard.writeText(gameId)
  }
  


  const renderPlayingGame = () => (
    <DrawBoard board={board} boardString={boardString} move = {move} color = {color} MakeMove = {MakeMove} error = {error} GameEnd = {false}/>
  );

  const renderGameEnd = () => (
    <div>
      <DrawBoard board={board} boardString={boardString} move = {false} color = {color} MakeMove = {MakeMove} error = {error} GameEnd = {true}/>
      <GameEnd draw={draw} win={win} error={error} onRestart={() => window.location.reload()} onHome={() => navigate("/")}/>
    </div>
  );  
  const renderLoading = () => (
    <div>
      <p class = "p1">Loading!</p>

    </div>
  );
  const renderNoRoom = () => (
    <div>
      <p class = "p1">No room found</p>

    </div>
  );

  const MakeMove = (move) => {

    socket.emit('move', { 'gameId': gameId, 'move': move - 1 });
  };



  let uiComponent;
  switch (gameState) {
    case 'no_room_found':
      uiComponent = renderNoRoom();
      break;
    case 'loading':
      uiComponent = renderLoading();
      break;
    case 'waiting_for_one_player':
      uiComponent = renderWaitingForOnePlayer();
      break;
    case 'playing_game':
      uiComponent = renderPlayingGame();
      break;
    case 'game_end':
      uiComponent = renderGameEnd();
      break;
    default:
      uiComponent = null;
  }

  return (
    <div>
      {uiComponent}

    </div>
  );
};




export default Room;