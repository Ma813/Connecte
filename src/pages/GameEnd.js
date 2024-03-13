import React from 'react';
import '../styles/GameEnd.css';

const GameEnd = ({ draw, win, onRestart, onHome}) => {
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
        <button onClick={onRestart}>Play Again</button>
        <button onClick={onHome}>Home</button>
      </div>
    </div>
  );
};

export default GameEnd;
