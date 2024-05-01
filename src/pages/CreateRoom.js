import React, { useState, useEffect } from 'react';
import { Route, useNavigate } from 'react-router-dom';
import '../styles/Room.css'; // Assuming the CSS file is in the same folder
import '../styles/Default.css'
import path from '../Path'

const GameRoom = () => {
    const [roomId, setRoomId] = useState('');
    const navigate = useNavigate();
    const [inputValue, setInputValue] = useState('');
    const [width, setWidth] = useState(7);
    const [heigth, setHeigth] = useState(6);
    const [gameMode, setGameMode] = useState(1);
    const [winCondition, setWinCondition] = useState(4);
    const [playerCondition, setPlayerCondition] = useState(2);
    

    const [errorMessage, setErrorMessage] = useState('');
    const [botDifficulty, setBotDifficulty] = useState(1);
    const [Loading, setLoading] = useState(false);





    useEffect(() => {
        if (roomId !== '') {
            navigate(`/room/${roomId}`);
        }
    }, [roomId]);

    const handleCreateRoomClick = () => {
        createRoom();
    };

    const handleSubmit = () => {
        createRoom();
    };

    const handleHeightChange = (e) => {
        const newHeight = parseInt(e.target.value, 10);
        if (newHeight >= 3 && newHeight <= 15) {
            setHeigth(newHeight);
            setErrorMessage(''); // Clear any previous error message
        } else {
            setErrorMessage('Height must be between 3 and 15.'); // Display error message
        }
    };
    const handleWidthChange = (e) => {
        const newWidth = parseInt(e.target.value, 10);
        if (newWidth >= 3 && newWidth <= 15) {
            setWidth(newWidth);
            setErrorMessage(''); // Clear any previous error message
        } else {
            setErrorMessage('Width must be between 3 and 15.'); // Display error message
        }
    };

    /* CHATBOTAS SAKE KAZKA TOKIO REIKE IDETI
const register = async () => {
    const userData = {
      mode: gameMode,
      winCondition: winCondition  // Sending win condition to the server
    };

    try {
      const response = await fetch(path + '/getRoom', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      const responseData = await response.json();
      if(responseData.error) throw new Error(responseData.error);
      setRoomId(responseData.gameId);
      navigate(`/room/${responseData.gameId}`);
    } catch (error) {
      console.error('Error creating/joining room:', error);
      // Handle error state appropriately
    }
};
    */
    const createRoom = async () => {
        setLoading(true);
        const userData = {
            mode: gameMode,
            playerCount: playerCondition,
            w: width,
            h: heigth,
            winCondition: winCondition

        };


        const response = await fetch(path + '/getRoom', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const responseData = await response.json();
        if (responseData.error === 'Gamemode does not exist') throw Error(responseData.error)
        setRoomId(responseData.gameId);
        navigate(`/room/${responseData.gameId}`);
    };

    const handleJoinRoomClick = () => {
        if (inputValue !== '') {
            navigate(`/room/${inputValue}`);
        }

        else {
            document.getElementById('roomIdInput').placeholder = 'Please insert room ID'
            document.getElementById('roomIdInput').className = 'errorMessage'
        }

    }

    const handleChange = (event) => {
        document.getElementById('roomIdInput').placeholder = 'Input Room ID'
        document.getElementById('roomIdInput').className = 'roomUIelement'
        setInputValue(event.target.value);
    };
    
    const renderLoading = () => (
        <div>
          <p class = "p1">Loading!</p>
    
        </div>
      );
    if(Loading){
        return renderLoading
    }
    else{
    return (
        <div>
            <div><button className='roomUIelement' onClick={handleCreateRoomClick}>Create Game Room</button></div>
            <form onSubmit={handleSubmit}>
                <div className='select'>
                    <input onChange={() => setGameMode(1)} type="radio" id="standardGameCheck" name="gameMode" value="standardGame" checked={gameMode === 1}></input>

                    <label htmlFor="standardGameCheck"> Standard game</label>
                </div>
                <div className='select'>
                    <label htmlFor="winConditionInput">Number of players:</label>
                    <input
                        id="playerInput"
                        type="number"
                        value={playerCondition}
                        onChange={e => setPlayerCondition(parseInt(e.target.value, 10))}
                        min="2"  // Minimum of 3 to make it reasonable
                        max="4"
                    />
                </div>
                <div className='select'>
                    <input onChange={() => setGameMode(2)} type="radio" id="memoryGameCheck" name="gameMode" value="memoryGame" checked={gameMode === 2}></input>

                    <label htmlFor="memoryGameCheck"> Memory Game</label>
                </div>
                <div className='select'>
                <input onChange={() => setGameMode(3)} type="radio" id="botGameCheck" name="gameMode" value="botGame" checked={gameMode === 3}></input>
                    <label htmlFor="botGameCheck"> Bot Game</label>
                    {gameMode === 3 && (
                        <div>
                            <label htmlFor="botDifficultySlider">Bot Difficulty:</label>
                            <input
                                id="botDifficultySlider"
                                type="range"
                                min="1"
                                max="10"
                                value={botDifficulty}
                                onChange={(e) => setBotDifficulty(parseInt(e.target.value, 10))}
                                style={{ width: "300px" }} // Optional style to improve visibility
                            />
                            <div className="sliderValue">
                                {botDifficulty} / 10
                            </div>
                        </div>
                    )}
                </div>
                <div className='select'>
                    <label htmlFor="heigthInput">Heigth of the board:</label>
                    <input
                        id="heigthInput"
                        type="number"
                        value={heigth}
                        onChange={handleHeightChange}
                        min="3"
                        max="15"
                    />
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                </div>
                <div className='select'>
                    <label htmlFor="widthInput">Length of the board:</label>
                    <input
                        id="widthInput"
                        type="number"
                        value={width}
                        onChange={handleWidthChange}
                        min="3"
                        max="15"
                    />
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                </div>

                   
           
                

                <div className='select'>
                    <label htmlFor="winConditionInput">Number of circles to connect to win:</label>
                    <input
                        id="winConditionInput"
                        type="number"
                        value={winCondition}
                        onChange={e => setWinCondition(parseInt(e.target.value, 10))}
                        min="2"  // Minimum of 3 to make it reasonable
                    />
                </div>
            </form>
            <div><input id='roomIdInput' className='roomUIelement' type="text" value={inputValue} onChange={handleChange} placeholder='Input Room ID'></input></div>
            <div><button className='roomUIelement' onClick={handleJoinRoomClick}>Join Game Room</button></div>
        </div>
        
    );
  }                 
};

export default GameRoom;