import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const Room = () => {
  const { roomId } = useParams();
  const [roomInfo, setRoomInfo] = useState(null);
  const [roomState, setRoomState] = useState(null);
  // Simulating fetching room information from an API
  useEffect(() => {
    // Fetch room information using the roomId
    // Replace this with your actual API call
    const fetchRoomInfo = async () => {
      try {
        // Simulating API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        // Simulated room data
        const roomData = {
          id: roomId,
          name: "Example Room",
          // Other room information...
        };

        // Set room information in state
        setRoomInfo(roomData);
      } catch (error) {
        console.error('Error fetching room information:', error);
      }
    };

    fetchRoomInfo();
  }, [roomId]);

  if (!roomInfo) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h2>Room Information</h2>
      <p>ID: {roomInfo.id}</p>
      <p>Name: {roomInfo.name}</p>
      {/* Display other room information as needed */}
    </div>
  );
};

export default Room;