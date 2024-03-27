import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Cookies from 'universal-cookie';

const cookies = new Cookies(null, { path: '/' });

function getCookie(name) {
  let cookie = cookies.get(name)
  if(cookie  === undefined)return null;
  return cookie
};

const ProfilePage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [winCount, setWinCount] = useState('');
  const [drawCount, setDrawCount] = useState('');
  const [loseCount, setLoseCount] = useState('');

  const { isAuthenticated } = useAuth(); // Assuming 'user' contains the logged-in user's details
  


  if (!isAuthenticated) {
    return (
      <div className="container mt-5 text-center">
        <p className="text-secondary">You must be logged in to view this page.</p>
      </div>
    );
  }
  const handleSubmit = async () => {
  const userData = {
      token: getCookie('token'),
    };
  const response = await fetch('http://' + window.location.hostname + ':5000/stats', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });

  const responseData = await response.json();
  const data = responseData.message
  setEmail(data.email)
  setUsername(data.username)
  setWinCount(data.winCount)
  setDrawCount(data.drawCount)
  setLoseCount(data.loseCount)
  }
  handleSubmit()
  return (
    <div className="container mt-5 text-light p-4 rounded">
      <h2 className="text-center mb-4">Profile Information</h2>
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 text-md-left text-center">
          {/* Name and Email Information */}
          <p><strong>Name:</strong> {username}</p>
          <p><strong>Email:</strong> {email}</p>
          <p><strong>Win count:</strong> {winCount}</p>
          <p><strong>Draw count:</strong> {drawCount}</p>
          <p><strong>Lose count:</strong> {loseCount}</p>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
