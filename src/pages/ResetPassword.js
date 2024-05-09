import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/LoginPage.css';
import path from '../Path'

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Reset error
        setError('');
        const userData = {
            username: email,
        };

        const response = await fetch(path + '/forgotPassword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const responseData = await response.json();

        if (responseData.error) {
            setSuccess('')
            return setError(responseData.error);
        }
        if (responseData.message) {
            setError('')
            return setSuccess(responseData.message);
        }
    };

    return (
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
                                    <label className="text-secondary" htmlFor="name">Username</label>
                                    <input type="text" className="form-control" id="name" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                </div>
                                <button type="submit" className="btn btn-primary bg-dark">Send new password</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
