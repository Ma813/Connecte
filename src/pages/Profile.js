import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Cookies from 'universal-cookie';
import path from '../Path'

const cookies = new Cookies(null, { path: '/' });

function getCookie(name) {
  let cookie = cookies.get(name)
  if (cookie === undefined) return null;
  return cookie
};

const ProfilePage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [winCount, setWinCount] = useState('');
  const [drawCount, setDrawCount] = useState('');
  const [loseCount, setLoseCount] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [games, setGames] = useState([{}]);
  const [gameTable, setGameTable] = useState({});
  const colors = ['red', 'yellow', 'TBD', 'TBD'];

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
    const response = await fetch(path + '/stats', {
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
    setGames(data.games)
  }

  //TODO: Make this into a nice table
  const renderGamesTable = (games) => {
    console.log(games)
    return (
      <table className="table table-dark table-striped">
        <thead>
          <tr>
            <th scope="col">W/D/L</th>
            <th scope="col">Time</th>
            <th scope="col">Color</th>
            <th scope="col">Opponent(s)</th>
            <th scope="col">Board</th>
          </tr>
        </thead>
        <tbody>
          {games.map((game, index) => (
            <tr>
              <td>{game.WDL}</td>
              <td>{game.time}</td>
              <td>{colors[game.which_turn - 1]}</td>
              <td>{game.opponents}</td>
              <td>{game.board}</td>
              {/* The last cell should be a button which when clicked shoes the board */}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

          if (!loaded) {
            console.log("loading...")
    handleSubmit()
          setLoaded(true)
  }
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
                {renderGamesTable(games)}
              </div>
            </div>
          </div>
          );
};

          export default ProfilePage;
