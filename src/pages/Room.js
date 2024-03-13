import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';
import '../styles/Default.css'
import '../styles/Connect4Board.css'


const Room = () => {
  const { gameId } = useParams();
  const [socket, setSocket] = useState(null);
  const [board, setBoard] = useState(null);
  const [move, setMove] = useState(null);
  const [error, setError] = useState(null);
  const [win, setWin] = useState(false)
  const [draw, setDraw] = useState(false)
  const [gameState, setGameState] = useState('loading');

  const fullURL = window.location.href;

  let board1 = new Array(6).fill(null)
    .map(i => new Array(7).fill(null));



  useEffect(() => {
    // Establish a WebSocket connection to the server
    const newSocket = io(window.location.hostname + ':5000'); // Replace with your server address
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected to server');
      newSocket.emit('join', { 'gameId': gameId });
    });

    newSocket.on('message', (data) => {
      const state = data['state'];
      //console.log(data)
      if (state == 'playing_game') {
        setBoard(data['board']);
        setMove(data['move']);
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
      }


      setGameState(state);

    });

    return () => {
      // Clean up: disconnect the WebSocket when the component unmounts
      newSocket.disconnect();
    };
  }, [gameId]);

  const MakeMove = (move) => {

    socket.emit('move', { 'gameId': gameId, 'move': move - 1 });
  };


  const renderWaitingForOnePlayer = () => (
    <div>
      <p className='message'>Waiting for one more player to join...</p>
      <p className='message'>Room ID is: <b>{gameId}</b></p>
      <p className='message'>Invite players with this URL: <b>{fullURL}</b> </p>
      <button className='copyButton' onClick={copyURL}>Copy URL</button>
      <button className='copyButton' onClick={copyID}>Copy Room ID</button>
    </div>

  );


 
  const reversedString = () => {
    
    return '[' + board.match(/\[([^[\]]*)\]/g).reverse().join(',') + ']';

  }

  const cleanedString = () => {
    return reversedString().replace(/[^0-2]/g, '');
  }


  const renderBoard = (board1) => {
    let i = 0;
    for (let rowIndex = 0; rowIndex < board1.length; rowIndex++) {

      for (let colIndex = 0; colIndex < board1[rowIndex].length; colIndex++) {

        const value = cleanedString()[i];
        if (value === "0") {
          if(move){
            board1[rowIndex][colIndex] = 'empty';
          }
          else{
            board1[rowIndex][colIndex] = 'empty2';
          }
        } else if (value === "1") {
          board1[rowIndex][colIndex] = 'red';
        } else if (value === "2") {
          board1[rowIndex][colIndex] = 'yellow';
        }
        i++;
      }
    }

    return (
      <div className="connect4-board">

        {move&&(board1.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={colIndex}
                className={`circle ${cell || 'empty'}`}
                onClick={() => handleCellClick(colIndex)}
              ></div>
            ))}
          </div>
        )))}
        {!move&&(board1.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={colIndex}
                className={`circle ${cell || 'empty'}`}
              ></div>
            ))}
          </div>
        )))}
      </div>

    )
  }

  const handleCellClick = (column) => {
    console.log("Clicked cell");
    MakeMove(column + 1);
  }

  const copyURL = () => {
    navigator.clipboard.writeText(fullURL)
  }
  const copyID = () => {
    navigator.clipboard.writeText(gameId)
  }


  const renderPlayingGame = () => (
    <div>

      <div>
        {move && (
          <div>
            <p class = "p1">Your turn</p>
          </div>
        )}

        {!move && (
          <div>
            <p class = "p1">Opponents turn</p>
          </div>
        )}
        
        {renderBoard(board1)}

      </div>

      <p class="error">{error}</p>

    </div>
  );

  const renderGameEnd = () => (
    <div>
      <p class = "p1">Game over!</p>
      {renderBoard(board1)}
      {draw && (
        <div>
          <p class = "p1">Draw</p>
        </div>
      )}
      {!draw && win && (
        <div>
          <p class = "p1">You won</p>
        </div>
      )}
      {!draw && !win && (
        <div>
          <p class = "p1">You lost</p>
        </div>
      )}
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
