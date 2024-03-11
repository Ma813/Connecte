import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const GameRoom = () => {
    const [roomId, setRoomId] = useState('');
    const navigate = useNavigate();

    const createRoom = () => {
        fetch('/getRoom')
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
      
    return (
        <div>
            <button onClick={handleCreateRoomClick}>Create Game Room</button>
        </div>
    );
};

export default GameRoom;