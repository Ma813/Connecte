import React, { useState } from 'react';
import {useParams } from 'react-router-dom';
import path from '../Path';

const Verify = () => {
    const [loaded, setLoaded] = useState(false);
    const [state, setState] = useState('loading...');

    const verifyID = useParams().verifyID;

    const handleSubmit = async () => {
        const userData = {
          id: verifyID,
        };
        const response = await fetch(path + '/verify', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData)
        });

        const responseData = await response.json();
        setState(responseData.message);
    }

    const renderLoading = () => {
        return (
            <div>
                <p>Loading...</p>
            </div>
        )
    }

    const renderSuccess = () => {
        return (
            <div>
                <p>Thank you for veryfing your email!</p>
            </div>
        )
    }

    if (!loaded) {
        handleSubmit()
        setLoaded(true)
    }

    return (
        <div>
            <h1>Verify</h1>
            <p> { state } </p>
        </div>
    )
}

export default Verify;