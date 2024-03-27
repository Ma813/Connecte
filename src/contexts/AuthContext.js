// src/contexts/AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  const login = (userData) => {
    // Implement login logic here, e.g., calling backend, storing the token
    setIsAuthenticated(true);
    setUser(userData);
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
      setIsAuthenticated(true);
      setUser(userData);

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
