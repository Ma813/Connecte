import React, { useState, useEffect } from 'react';
import { Route, useNavigate } from 'react-router-dom';
import '../styles/Room.css'; // Assuming the CSS file is in the same folder
import '../styles/Default.css'
import path from '../Path'

const GameRoom = () => {
    const [roomId, setRoomId] = useState('');
    const navigate = useNavigate();
    const [inputValue, setInputValue] = useState('');
    const [gameMode, setGameMode] = useState(1);
    const [winCondition, setWinCondition] = useState(4);





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
        const userData = {
            mode: gameMode
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

    return (
        <div>
            <div><button className='roomUIelement' onClick={handleCreateRoomClick}>Create Game Room</button></div>
            <form onSubmit={handleSubmit}>
                <div className='select'>
                    <input onChange={() => setGameMode(1)} type="radio" id="standardGameCheck" name="gameMode" value="standardGame" checked={gameMode === 1}></input>
                    
                    <label   htmlFor="standardGameCheck"> Standard game</label>
                </div>
                <div className='select'>
                    <input onChange={() => setGameMode(2)} type="radio" id="memoryGameCheck" name="gameMode" value="memoryGame" checked={gameMode === 2}></input>
                    
                    <label htmlFor="memoryGameCheck"> Memory Game</label>
                </div>
                <div className='select'>
                    <input onChange={() => setGameMode(3)} type="radio" id="botGameCheck" name="gameMode" value="botGame" checked={gameMode === 3}></input>
                    
                    <label htmlFor="botGameCheck"> Bot Game</label>
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
};

export default GameRoom;