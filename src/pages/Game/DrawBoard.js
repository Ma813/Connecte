import React from 'react';
import '../../styles/GameEnd.css';



const colors = {
    '1': 'rgb(255,0,0)',
    '2': 'rgb(255,255,0)',
    '3': 'rgb(0,0,255)',
    '4': 'rgb(0,255,0)',
    '0': 'rgb(255,255,255)'
}





const DrawBoard = ({ board, boardString, move, color, MakeMove, error, gameEnd }) => {
    const reversedString = () => {
        return '[' + boardString.match(/\[([^[\]]*)\]/g).reverse().join(',') + ']';
    }

    const cleanedString = () => {
        return reversedString().replace(/[^0-2]/g, '');
    }

    const handleCellClick = (event, column) => {
        if (event.currentTarget.className.includes("hoverable"))
            event.currentTarget.style.background = 'white';
        MakeMove(column + 1);
    }

    const MouseOver = (event) => {
        if (event.currentTarget.className.includes("hoverable") && move) {
            event.currentTarget.style.background = colors[color];
        }
    }

    const MouseOut = (event) => {
        if (event.currentTarget.className.includes("hoverable"))
            event.currentTarget.style.background = 'white';
    }



    const renderBoard = (board) => {
        let i = 0;
        for (let rowIndex = 0; rowIndex < board.length; rowIndex++) {
            for (let colIndex = 0; colIndex < board[rowIndex].length; colIndex++) {
                const value = cleanedString()[i];
                board[rowIndex][colIndex] = value;
                i++;
            }
        }

        return (
            <div className="connect4-board">
                {move && (

                    <p class="p1">Your turn</p>

                )}
                {!move && (

                    <p class="p1">Opponents turn</p>

                )}
                <div
                    class="smallCircle"
                    style={{ backgroundColor: colors[color] }}
                ></div>

                {(board.map((row, rowIndex) => (
                    <div key={rowIndex} className="row">
                        {row.map((cell, colIndex) => (
                            <div
                                key={colIndex}
                                className={`circle ${cell == "0" && "hoverable"}`}
                                onClick={move ? ((event) => handleCellClick(event, colIndex)) : (void 0)}
                                style={{ backgroundColor: colors[cell] }}
                                onMouseOver={((event) => MouseOver(event))}
                                onMouseOut={(event) => MouseOut(event)}
                            ></div>
                        ))}
                    </div>
                )))}

            </div>

        )
    }

    return (
        <div>
             
            <div>
                {renderBoard(board)}
            </div>
            {move&&(<p class="error">{error}</p>)}
        </div>
    );
};

export default DrawBoard;
