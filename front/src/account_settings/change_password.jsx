import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contextProvider';

const ChangePassword = () => {
  const navigate = useNavigate();
  const {setAccessToken}= useAuth();
  const [errorMessage, setErrorMessage] = useState('');
  const [passwords, setPasswords] = useState({
    current: '',
    new: '',
    verify: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPasswords((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (passwords.new !== passwords.verify) {
      setErrorMessage('New password does not match');
      return;
    }

    const accessToken = localStorage.getItem('accessToken');
    try {
      const response = await fetch('http://127.0.0.1:8000/change_password', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({ current: passwords.current, new: passwords.new })
      });

      if (response.ok) {
        localStorage.removeItem('accessToken');
        setAccessToken(null);
        navigate('/SignIn');
      } else {
        setErrorMessage('Failed to change password');
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      {errorMessage && <h3 className="error-message">{errorMessage}</h3>}
      <form onSubmit={handleSubmit}>
        <div className='form-row'>
          <label htmlFor="current" className='form-label'>Current Password</label>
          <input
            type="password"
            className='form-input'
            id="current"
            name="current"
            value={passwords.current}
            onChange={handleChange}
          />
          <label htmlFor="new" className='form-label'>New Password</label>
          <input
            type="password"
            className='form-input'
            id="new"
            name="new"
            value={passwords.new}
            onChange={handleChange}
          />
          <label htmlFor="verify" className='form-label'>Verify New Password</label>
          <input
            type="password"
            className='form-input'
            id="verify"
            name="verify"
            value={passwords.verify}
            onChange={handleChange}
          />
        </div>
        <button className='btn'>Change</button>
      </form>
    </div>
  );
};

export default ChangePassword;
