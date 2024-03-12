import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';
import '../styles/Connect4Board.css'

const Room = () => {
    const { gameId } = useParams();
    const [socket, setSocket] = useState(null);
    const [board, setBoard] = useState(null);
    const [move, setMove] = useState(null);
    const [error, setError] = useState(null);
    const [win,setWin] = useState(false)
    const [draw,setDraw] = useState(false)
    const [gameState, setGameState] = useState('loading');
    

    let board1 = new Array(6).fill(null)
    .map(i => new Array(7).fill(null));
  


    useEffect(() => {
        // Establish a WebSocket connection to the server
        const newSocket = io(window.location.hostname+':5000'); // Replace with your server address
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

  
 // const dataString = board // should be board
    const reversedString = () => {
      //return board.replace(/[^0-2]/g, '');
      return '[' + board.match(/\[([^[\]]*)\]/g).reverse().join(',') + ']';

    }

    const cleanedString = () =>{
      return reversedString().replace(/[^0-2]/g, '');
    }
    //const newString = cleanedString();
    //const cleanedString = dataString.replace(/[^0-2\s]/g, '');
  
  const renderBoard = (board1) => {
    let i = 0;
    for (let rowIndex = 0; rowIndex < board1.length; rowIndex++) {

      for (let colIndex = 0; colIndex < board1[rowIndex].length; colIndex++) {

        const value = cleanedString()[i];
        if (value === "0") {
          board1[rowIndex][colIndex] = 'empty';
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
      
    {board1.map((row, rowIndex) => (
      <div key={rowIndex} className="row">
        {row.map((cell, colIndex) => (
          <div
            key={colIndex}
            className={`circle ${cell || 'empty'}`}
            
          ></div>
        ))}
      </div>
    ))}
  </div>

    )
  }

  



  const renderPlayingGame = () => (
    <div>
      <p>Game in progress...
      </p>
      <div>
        {cleanedString()}
      {renderBoard(board1)}

      </div>
      
      {board}
      {error}
      {move && (
       <div>
          <p>Your turn</p>
          <button onClick={() => {MakeMove(1); renderBoard(board1);}}>1</button>
          <button onClick={() => {MakeMove(2); renderBoard(board1);}}>2</button>
          <button onClick={() => {MakeMove(3); renderBoard(board1);}}>3</button>
          <button onClick={() => {MakeMove(4); renderBoard(board1);}}>4</button>
          <button onClick={() => {MakeMove(5); renderBoard(board1);}}>5</button>
          <button onClick={() => {MakeMove(6); renderBoard(board1);}}>6</button>
          <button onClick={() => {MakeMove(7); renderBoard(board1);}}>7</button>
        </div>
      )}
    
    </div>
  );

  const renderGameEnd = () => (
    <div>
      <p>Game over!</p>
      {renderBoard(board1)}
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
/*<div className="connect4-board">
      
        {board1.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={colIndex}
                className={`circle ${cell || 'empty'}`}
                
              ></div>
            ))}
          </div>
        ))}
      </div>*/


      /*<div>
      {board1.map((row, rowIndex) => (
  <div key={rowIndex} className="row">
    {row.map((cell, colIndex) => (
      <div
        key={colIndex}
        className={`circle ${cell === null ? 'empty' : `player-${cell}`}`}
      ></div>
    ))}
  </div>
))}
      </div>*/