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
	

    const createRoom = () => {
        fetch(path+'/getRoom')
            .then(response => response.json())
            .then(data => {
                // Set the API data to the state variable
                setRoomId(data.gameId);
                navigate(`/room/${data.gameId}`);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    };
	

    useEffect(() => {
    if (roomId !== '') {
        navigate(`/room/${roomId}`);
      }
    }, [roomId]);

    const handleCreateRoomClick = () => {
		register();
    };
	
	const handleSubmit = () => {
        register();
    };
	
	const register = async () => {
    const userData = {
      mode: gameMode
    };

  
      const response = await fetch(path +'/getRoom', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      const responseData = await response.json();
      if(responseData.error === 'Gamemode does not exist') throw Error(responseData.error)
	  setRoomId(responseData.gameId);
      navigate(`/room/${responseData.gameId}`);
  };

    const handleJoinRoomClick = () => {
        if (inputValue !== '')
        {
            navigate(`/room/${inputValue}`);
        }

        else
        {
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
			<div><input onChange={() => setGameMode(1)} type="radio" id="standardGameCheck" name="standardGameCheck" value="standardGame" checked="checked"></input>
			<label for="standardGameCheck"> Standard game</label></div>
			<div><input onChange={() => setGameMode(2)} type="radio" id="memoryGameCheck" name="standardGameCheck" value="memoryGame"></input>
			<label for="memoryGameCheck"> Memory Game</label></div>
			</form>
            <div><input id='roomIdInput' className='roomUIelement' type="text" value={inputValue} onChange={handleChange} placeholder='Input Room ID'></input></div>
            <div><button className='roomUIelement' onClick={handleJoinRoomClick}>Join Game Room</button></div>
        </div>
        

    );
};

export default GameRoom;