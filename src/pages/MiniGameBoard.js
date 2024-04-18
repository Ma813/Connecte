import React from 'react';
import '../styles/ProfileGameBoard.css';


const colors = {
    '1': 'rgb(255,0,0)',
    '2': 'rgb(255,255,0)',
    '3': 'rgb(0,0,255)',
    '4': 'rgb(0,255,0)',
	'5': 'rgb(255,122,0)',
    '0': 'rgb(255,255,255)'
};

const MiniGameBoard = ({ board }) => {
    const renderBoard = (board) => {
        return (
            <div className="profile-connect4-board">
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} className="profile-row">
                        {row.map((cell, colIndex) => (
                            <div
                                key={colIndex}
                                className="profile-circle"
                                style={{ backgroundColor: colors[cell] }}
                            ></div>
                        ))}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="profile-game-board-container">
            {renderBoard(board)}
        </div>
    );
};

export default MiniGameBoard;
