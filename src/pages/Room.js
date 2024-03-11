import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';

const Room = () => {
    const { gameId } = useParams();
    const [socket, setSocket] = useState(null);
    const [board, setBoard] = useState(null);
    const [move, setMove] = useState(null);
    const [error, setError] = useState(null);
    const [win,setWin] = useState(false)
    const [draw,setDraw] = useState(false)
    const [gameState, setGameState] = useState('loading');
    useEffect(() => {
        // Establish a WebSocket connection to the server
        const newSocket = io('http://localhost:5000'); // Replace with your server address
        setSocket(newSocket);

        newSocket.on('connect', () => {
          console.log('Connected to server');
          newSocket.emit('join', { 'gameId': gameId }); 
        });
        
        newSocket.on('message', (data) => {
          const state = data['state'];
          console.log(data)
          if(state == 'playing_game'){
            setBoard(data['board']);
            setMove(data['move']);
            if('error' in data){
              setError(data['error'])
            }
            else{
              setError(null)
            }
          }
          if(state == 'game_end'){
            setBoard(data['board']);
            setMove(data['move']);
            setWin(data['winner'])
            setDraw(data['draw'])
          }
         
          
          setGameState(state);
          
      });

        return () => {
            // Clean up: disconnect the WebSocket when the component unmounts
            newSocket.disconnect();
        };
    }, [gameId]);

    const MakeMove = (move) => {
     
      socket.emit('move', { 'gameId': gameId,'move': move-1 }); 
    };
  

  const renderWaitingForOnePlayer = () => (
    <div>
      <p>Waiting for one more player to join...</p>
      {/* Add any relevant UI elements */}
    </div>

  );

  const renderPlayingGame = () => (
    <div>
      <p>Game in progress...
      </p>
      {board}
      {error}
      {move && (
       <div>
          <p>Your turn</p>
          <button onClick={() => MakeMove(1)}>1</button>
          <button onClick={() => MakeMove(2)}>2</button>
          <button onClick={() => MakeMove(3)}>3</button>
          <button onClick={() => MakeMove(4)}>4</button>
          <button onClick={() => MakeMove(5)}>5</button>
          <button onClick={() => MakeMove(6)}>6</button>
          <button onClick={() => MakeMove(7)}>7</button>
        </div>
      )}
    
    </div>
  );

  const renderGameEnd = () => (
    <div>
      <p>Game over!</p>
      {board}
      {draw && (
       <div>
          <p>Draw</p>
        </div>
      )}
      {!draw && win && (
       <div>
          <p>You won</p>
        </div>
      )}
      {!draw && !win && (
       <div>
          <p>You lost</p>
        </div>
      )}
    </div>
  );
  const renderLoading = () => (
    <div>
      <p>Loading!</p>
      {/* Display game results or options for starting a new game */}
    </div>
  );
  const renderNoRoom = () => (
    <div>
      <p>No room found</p>
      {/* Display game results or options for starting a new game */}
    </div>
  );

  // Determine which UI component to render based on game state
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
      {/* Add event handlers or buttons to trigger state changes */}
    </div>
  );
};



export default Room;
