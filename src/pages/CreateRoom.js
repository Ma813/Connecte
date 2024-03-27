import React, { useState, useEffect } from 'react';
import { Route, useNavigate } from 'react-router-dom';
import '../styles/Room.css'; // Assuming the CSS file is in the same folder
import '../styles/Default.css'
import path from '../Path'

const GameRoom = () => {
    const [roomId, setRoomId] = useState('');
    const navigate = useNavigate();
    const [inputValue, setInputValue] = useState('');
    

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
        createRoom();
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
            <div><input id='roomIdInput' className='roomUIelement' type="text" value={inputValue} onChange={handleChange} placeholder='Input Room ID'></input></div>
            <div><button className='roomUIelement' onClick={handleJoinRoomClick}>Join Game Room</button></div>
        </div>
        

    );
};

export default GameRoom;