import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/LoginPage.css';
import path from '../Path'
import { useParams } from 'react-router-dom';


const ResetPasswordLink = () => {
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loaded, setLoaded] = useState(false);
    const [linkValid, setLinkValid] = useState(false);

    const resetLink = useParams().link;


    const handleLoad = async (e) => {
        setError(''); // Reset error message

        const userData = {
            link : resetLink
        };

        const response = await fetch(path + '/validateResetLink', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const responseData = await response.json();
        console.log(responseData);
        setLinkValid(responseData.linkValid);
        if (responseData.error) {
            setError(responseData.error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Reset error message
        setSuccess(''); // Reset success message
        console.log(newPassword, confirmPassword)
        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        // Send the data to the server

        const userData = {
            link: resetLink,
            password: newPassword
        };

        const response = await fetch(path + '/resetPassword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        const responseData = await response.json();
        console.log(responseData);
        if (responseData.error) {
            setError(responseData.error);
        } else {
            setSuccess(responseData.message);
        }
    };

    if (!loaded) {
        handleLoad();
        setLoaded(true);
    }
    const renderReset = () => (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <h5 className="card-header bg-dark">Reset Password</h5>
                        <div className="card-body">
                            {error && <div className="alert alert-danger" role="">{error}</div>}
                            {success && <div className="alert alert-success" role="">{success}</div>}
                            <form onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <div className="form-group">
                                        <label className="text-secondary" htmlFor="password">New Password</label>
                                        <input type="password" className="form-control" id="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                                    </div>
                                    <div className="form-group">
                                        <label className="text-secondary" htmlFor="confirmPassword">Confirm Password</label>
                                        <input type="password" className="form-control" id="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                                    </div>
                                </div>
                                <button type="submit" className="btn btn-primary bg-dark">Reset Password</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderInvalid = () => (
        <div className="container mt-5 text-center alert alert-danger h1">
            {error}
        </div>
    );



    return (
        (linkValid && renderReset()) || 
        (!linkValid && renderInvalid())
    );
};

export default ResetPasswordLink;
