import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Cookies from 'universal-cookie';
import path from '../Path'
import MiniGameBoard from './MiniGameBoard';
import PieChart from '../components/PieChart';
import "../styles/ProfilePage.css";

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
  const [chartData, setChartData] = useState(null);
  const { isAuthenticated } = useAuth(); // Assuming 'user' contains the logged-in user's details
  const navigate = useNavigate();
  const [showingBoard, setShowingBoard] = useState(false);
  const [board, setBoard] = useState(null);



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
    setChartData({
      labels: ['Wins', 'Draws', 'Losses'],
      datasets: [
        {
          label: 'Games',
          data: [data.winCount, data.drawCount, data.loseCount],

        }
      ]
    });
  }

  function convertBoardStringToArray(boardString) {
    if (!boardString) {
      console.error('Invalid or empty board string:', boardString);
      return []; // Return an empty array as a fallback
    }

    try {
      // Step 1: Remove all periods and trim unnecessary whitespace
      let cleanedString = boardString.replace(/[\.,]|\./g, ' ').trim();

      let trimedString = cleanedString.substring(1, cleanedString.length - 1);

      // Step 2: Split the string into rows by the newline character
      let rows = trimedString.split('\n').map(row => row.trim());
      // Step 3: Remove the outer brackets and split each row into numbers
      rows = rows.map(row =>
        row.slice(1, row.length - 1) // Remove the '[' and ']' from each row
          .trim()
          .split(/\s+/) // Split the row by one or more spaces
          .map(Number) // Convert each element from string tmo number
      );

      return rows;
    } catch (error) {
      console.error('Error converting board string to array:', boardString, error);
      return [];
    }
  }

  const handleShowBoard = (board) => {
    setShowingBoard(true);
    setBoard(convertBoardStringToArray(board));
  };

  //TODO: Make this into a nice table
  const renderGamesTable = (games) => {
    //console.log(games)
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
              <td>
                <div className="profile-circle" style={{ backgroundColor: colors[game.which_turn - 1] }}></div>
              </td>
              <td>{game.opponents}</td>
              <td>
                {/* Convert string board to array and render */}
                <p className='blueLink' onClick={() => handleShowBoard(game.board)}>Show</p>
                {/* {game.board ? <MiniGameBoard board={convertBoardStringToArray(game.board)} /> : <p>No board data</p>} */}
              </td>
              {/*console.log(game.board)*/}
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

  const handleChangePass = () => {
    navigate('/forgot-password');
  }


  return (
    <div className="container mt-5 text-light p-4 rounded fullW">
      <h2 className="text-center mb-4">Profile page</h2>
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 text-center">
          {/* Name and Email Information */}

          <table className="table table-dark table-striped center">
            <thead>
              <tr>
                <th scope="col">Username</th>
                <th scope="col">Email</th>
                <th scope="col">Password</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{username}</td>
                <td>{email}</td>
                <td className='blueLink' onClick={handleChangePass}>Change</td>
              </tr>
            </tbody>
          </table>
          {chartData && <PieChart chartData={chartData} />}
          {renderGamesTable(games)}
        </div>
      </div>
      {showingBoard && board &&
        <div className="game-end-overlay">
          <div className="game-end-content">
            {<MiniGameBoard board={board} />}
            {<button onClick={() => setShowingBoard(false)}>Close</button>}
          </div>
        </div>
      }

    </div>
  );
};

export default ProfilePage;
