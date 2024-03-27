// src/contexts/AuthContext.js
import React, { createContext, useContext, useState } from 'react';
import Cookies from 'universal-cookie';


const AuthContext = createContext(null);

const cookies = new Cookies(null, { path: '/' });

const setCookie = (name,value) => {
  let d = new Date();
  d.setTime(d.getTime() + (12*60*60*1000));
  cookies.set(name, value, {path: "/", expires: d});
};

function getCookie(name) {
  let cookie = cookies.get(name)
  if(cookie  === undefined)return null;
  return cookie
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);


  const login =  async  (username, password) => {
    const userData = {
      username: username,
      hashed_pass: password,
    };

    console.log(userData);

    try {
      const response = await fetch('http://'+window.location.hostname+':5000/checkUser', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      const responseData = await response.json();
      setCookie('token',responseData.token)
      setIsAuthenticated(true);
    } catch (error) {
      setError('Error creating player:', error);
      console.log(error);
    }
   

  };

  const logout = () => {
    // Clear user session, e.g., removing token
    setIsAuthenticated(false);
    setUser(null);
  };

  const register = async (email, pass, username) => {
    const userData = {
      username: username,
      hashed_pass: pass,
      email: email,
    };

    try {
      const response = await fetch('http://' + window.location.hostname + ':5000/registerPlayer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      const responseData = await response.json();
      
      
    } catch (error) {
      setError('Error creating player:', error);
    }


  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => useContext(AuthContext);
