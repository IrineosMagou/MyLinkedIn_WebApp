import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import { useAuth } from '../contextProvider';
import Button from '../myreuse/myButton';
import jwtDecode from 'jwt-decode';

const SignIn = () => {
    let navigate = useNavigate(); // Use navigate instead of history
    const { setAccessToken , setIdPic } = useAuth(); 
    const [error, setError] = useState(null);
    const [userSignIn, setUserSignIn] = useState({
        username: '',
        password: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', userSignIn.username);
        formData.append('password', userSignIn.password);

        try {
            const response = await fetch('http://127.0.0.1:8000/token', {
                method: 'POST',
                mode: 'cors',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                const token = data.access_token;
                localStorage.setItem('accessToken', token);
                setAccessToken(token);
                const decodedToken = jwtDecode(token);
                console.log(decodedToken);
                const isAdmin = decodedToken.scopes;
                if(isAdmin.length == 2){
                    navigate('/admin_users');
                }else{
                    console.log(decodedToken.sub);
                    setIdPic(decodedToken.sub);
                    localStorage.setItem('id', decodedToken.sub);
                    navigate('/'); // Use navigate for redirection
                }
            } else {
                const data = await response.json();
                setError(data.detail || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            setError('An unexpected error occurred');
        }
    };

    const handleChange = (e) => {
        setUserSignIn({
            ...userSignIn,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div>
            <form className="form" onSubmit={handleSubmit}>
                <h3>Log In</h3>
                <div className='form-row'>
                    <label htmlFor="username" className='form-label'>
                        Email
                    </label>
                    <input
                        type="text"
                        className='form-input'
                        id='username'
                        name='username'
                        value={userSignIn.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className='form-row'>
                    <label htmlFor='password' className='form-label'>
                        Password
                    </label>
                    <input
                        type='password'
                        className='form-input'
                        id='password'
                        name='password'
                        value={userSignIn.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <Button label="Είσοδος" type="submit" /> {/* Use type="submit" */}
                {error && <div className="error-message">{error}</div>}
            </form>
        </div>
    );
};

export default SignIn;
