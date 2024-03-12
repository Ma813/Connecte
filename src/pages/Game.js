import React, { useState, useEffect } from 'react';



export default function Game() {
    
    function sendRequest(){
 
        // Simple POST request with a JSON body using fetch
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: 'React POST Request Example' })
      };
      fetch('http://'+window.location.hostname+':5000/send', requestOptions)
      
      }
      
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('http://'+window.location.hostname+':5000/time').then(res => res.json()).then(data => {
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