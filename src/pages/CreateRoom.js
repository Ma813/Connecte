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
    const [showSettings, setShowSettings] = useState(false);





    useEffect(() => {
        if (roomId !== '') {
            navigate(`/room/${roomId}`);
        }
    }, [roomId]);

    const handleCreateRoomClick = () => {
        if(heigth >= 3 && heigth <= 9 & width >= 3 && width <= 9 && winCondition > 1){
            createRoom();
        }
        else
        setErrorMessage('Height and width must be between 3 and 9 and number of circles should be at least 2.');
        return;
            
        
    };

    const handleSubmit = () => {
        createRoom();
    };

    const handleHeightChange = (e) => {
        const newHeight = parseInt(e.target.value, 10);
        
            setHeigth(newHeight);
            setErrorMessage(''); // Clear any previous error message
        
    };
    const handleWidthChange = (e) => {
        const newWidth = parseInt(e.target.value, 10);
        
            setWidth(newWidth);
            setErrorMessage(''); // Clear any previous error message
        
        
    };

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
        document.getElementById('roomIdInput').className = 'textInput'
        setInputValue(event.target.value);
    };

    const renderLoading = () => (
        <div>
            <p class="p1">Loading!</p>

        </div>
    );
    if (Loading) {
        return renderLoading
    }
    else {
        return (
            <div className='CreateRoomPage'>
                <div><button className='button-6' onClick={handleCreateRoomClick}>Create Game Room</button></div>
                <form onSubmit={handleSubmit} action="/action_page.php">
                    <label htmlFor="gameMode">Please select Game mode:</label>
                    <div className='select'>
                        <input onChange={() => setGameMode(1)} type="radio" id="standardGameCheck" name="gameMode" value="standardGame" checked={gameMode === 1}></input>
                        <label className="hoverLabel" htmlFor="standardGameCheck">
                            Standart game
                        </label>
                        <div className="hover-text"> Standart game of Connect4 where you may choose between 2 and 4 players to play against </div>

                    </div>
                    <div className='select'>
                        <input onChange={() => setGameMode(2)} type="radio" id="memoryGameCheck" name="gameMode" value="memoryGame" checked={gameMode === 2}></input>

                        <label className="hoverLabel" htmlFor="memoryGameCheck"> Memory Game</label>
                        <div className="hover-text"> Memory game of Connect4 where players can't see the colors of the tokens</div>
                    </div>
                    <div className='select'>
                        <input onChange={() => setGameMode(3)} type="radio" id="botGameCheck" name="gameMode" value="botGame" checked={gameMode === 3}></input>
                        <label className="hoverLabel" htmlFor="botGameCheck"> Bot Game</label>
                        <div className="hover-text"> A Connect4 game versus a bot, where You may choose bot difficulty</div>
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
                    <div className='settings'>
                        <label htmlFor="additionalSettings">Press to show additional settings:</label> <input onChange={() => setShowSettings(true)} type="radio" id="additionalSettings"  checked={showSettings === true}></input>
                        {showSettings && (
                            <div>
                                <div className='select'>
                                    <label htmlFor="heigthInput">Heigth:</label>
                                    <input
                                        className="numberInput"
                                        id="heigthInput"
                                        type="number"
                                        value={heigth}
                                        onChange={handleHeightChange}
                                        min="3"
                                        max="9"
                                    />
                                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                                </div>
                                <div className='select'>
                                    <label htmlFor="widthInput">Length:</label>
                                    <input
                                        className="numberInput"
                                        id="widthInput"
                                        type="number"
                                        value={width}
                                        onChange={handleWidthChange}
                                        min="3"
                                        max="9"
                                    />
                                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                                </div>





                                <div className='select'>
                                    <label htmlFor="winConditionInput">Number of circles:</label>
                                    <input
                                        className="numberInput"
                                        id="winConditionInput"
                                        type="number"
                                        value={winCondition}
                                        onChange={e => setWinCondition(parseInt(e.target.value, 10))}
                                        min="2"  // Minimum of 3 to make it reasonable
                                        max="9"
                                    />
                                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                                </div>

                                {gameMode === 1 && (
                            <div>
                                <label htmlFor="winConditionInput">Choose number of players:</label>
                                <input
                                    className="numberInput"
                                    id="playerInput"
                                    type="number"
                                    value={playerCondition}
                                    onChange={e => setPlayerCondition(parseInt(e.target.value, 10))}
                                    min="2"  // Minimum of 3 to make it reasonable
                                    max="4"
                                />
                            </div>
                        )}
                            </div>
                        )}
                    </div>
                </form>
                <div><input className='textInput' id='roomIdInput' type="text" value={inputValue} onChange={handleChange} placeholder='Input Room ID'></input></div>
                <div><button className='button-6' onClick={handleJoinRoomClick}>Join Game Room</button></div>
            </div>

        );
    }
};

export default GameRoom;