import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const ProfilePage = () => {
  const { user } = useAuth(); // Assuming 'user' contains the logged-in user's details

  if (!user) {
    return (
      <div className="container mt-5 text-center">
        <p className="text-secondary">You must be logged in to view this page.</p>
      </div>
    );
  }

  return (
    <div className="container mt-5 text-light p-4 rounded">
      <h2 className="text-center mb-4">Profile Information</h2>
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 text-md-left text-center">
          {/* Name and Email Information */}
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
