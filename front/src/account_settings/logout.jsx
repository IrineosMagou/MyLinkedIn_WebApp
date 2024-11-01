import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contextProvider'; // Import the context hook
import Button from '../myreuse/myButton';

const Logout = () => {
    const navigate = useNavigate(); // Use navigate instead of history
    const { setAccessToken , setIdPic } = useAuth(); // Get setAccessToken from context

    const handleClick = () => {
        localStorage.removeItem('accessToken');
        setAccessToken(null); // Clear the accessToken in context
        setIdPic(null); // Clear the accessToken in context
        navigate('/SignIn'); // Redirect to SignIn page
    };

    return (
        <div>
            <Button label="Αποσυνδεση" onClick={handleClick} />
        </div>
    );
};

export default Logout;
