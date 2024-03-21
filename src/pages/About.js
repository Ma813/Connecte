import '../styles/Default.css'
import { useState } from 'react';


export default function About() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const [error, setError] = useState("");


    const handleSubmit = async (event) => {
      event.preventDefault();
    const userData = {
        username: username,
        hashed_pass: pass,
        email: email,
      };

      console.log(userData);
  
      try {
        const response = await fetch('http://'+window.location.hostname+':5000/registerPlayer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
        });
  
        const responseData = await response.json();
        setError(responseData.message); // Output the response message
      } catch (error) {
        setError('Error creating player:', error);
        console.log(error);
      }
  };

    return (
        
        <div>
            <form onSubmit={handleSubmit}>
            <label>Username:
                <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                />
            </label>
            <label>email:
                <input 
                type="text" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                />
            </label>
            <label>pass:
                <input 
                type="text" 
                value={pass}
                onChange={(e) => setPass(e.target.value)}
                />
            </label>
            <input type="submit" />
            </form>

            <p>{error}</p>
            <h1>Connectė</h1>
                <p>Connectė is an implementation of the game Connect4 using React and Python flask. In the game you can play against other opponents or a bot that utilizes the alpha-beta pruning algorithm to select the moves that lead to the best outcome. The website also implements multiple game modes that would be impossible to play on a physical board.</p>
                <h2>Authors:</h2>
                <p>Martynas Mačiulaitis</p>
                <p>Martynas Jukna</p>
                <p>Dominykas Pranaitis</p>
                <p>Ainis Vaičiūnas</p>
                <p>Julius Barauskas</p>
                <p>Matas Gudliauskas</p>
        </div>
    )
}