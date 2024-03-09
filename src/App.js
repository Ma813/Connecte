import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';


function sendRequest(){
 
  // Simple POST request with a JSON body using fetch
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: 'React POST Request Example' })
};
fetch('/send', requestOptions)

}

function App() {




  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);
 
  return (
    <div className="App">
      <header className="App-header">
        <p>The current time is {currentTime}.</p>
      </header>
      <button onClick={sendRequest}>  Send request
      </button>
    </div>
    
  );
}

export default App;