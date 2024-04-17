import React from 'react';
import '../../styles/GameEnd.css';

const GameEnd = ({ draw, win, onRestart, onHome, error,name,spectator}) => {
  
  if(!spectator){
  return (
    <div className="game-end-overlay">
      <div className="game-end-content">
        <p>Game over!</p>
        {draw ? (
          <p>It's a draw!</p>
        ) : win ? (
          <p>Congratulations! You won!</p>

        ) : (
          <p>Sorry, you lost. Better luck next time!</p>
        )}
      
        <p className='error'>{error}</p>
        <button onClick={onRestart}>Play Again</button>
        <button onClick={onHome}>Home</button>
      </div>
    </div>
  );
        }
        else{
          return(
          <div className="game-end-overlay">
          <div className="game-end-content">
            <p>Game over!</p>
            {draw ? (
              <p>It's a draw!</p>
            ) :  (
              <p>User {name} won the game!</p>
            )
            }
            <p className='error'>{error}</p>
            <button onClick={onHome}>Home</button>
          </div>
        </div>
          )
        }
};

export default GameEnd;
