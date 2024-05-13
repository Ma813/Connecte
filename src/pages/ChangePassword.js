import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../styles/LoginPage.css';
import path from '../Path'
import Cookies from 'universal-cookie';

const cookies = new Cookies(null, { path: '/' });

function getCookie(name) {
    let cookie = cookies.get(name)
    if (cookie === undefined) return null;
    return cookie
};

const ChangePassword = () => {
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
          return setError('Passwords do not match');
        }
        
        setError(''); // Reset error message
        
        const userData = {
            token: getCookie('token'),
            oldPassword: oldPassword,
            newPassword: newPassword,
        };

        const response = await fetch(path + '/changePassword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const responseData = await response.json();
        console.log(responseData)
        if (responseData.success) {
            setSuccess(responseData.success)
            setError('')
        }
        if (responseData.error) {
            setSuccess('')
            setError(responseData.error)
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <h5 className="card-header bg-dark">Change Password</h5>
                        <div className="card-body">
                            {error && <div className="alert alert-danger" role="">{error}</div>}
                            {success && <div className="alert alert-success" role="">{success}</div>}
                            <form onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <div className="form-group">
                                        <label className="text-secondary" htmlFor="password">Old Password</label>
                                        <input type="password" className="form-control" id="oldPassword" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} required />
                                    </div>
                                    <div className="form-group">
                                        <label className="text-secondary" htmlFor="password">New Password</label>
                                        <input type="password" className="form-control" id="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                                    </div>
                                    <div className="form-group">
                                        <label className="text-secondary" htmlFor="confirmPassword">Confirm Password</label>
                                        <input type="password" className="form-control" id="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                                    </div>
                                </div>
                                <button type="submit" className="btn btn-primary bg-dark">Change</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChangePassword;
