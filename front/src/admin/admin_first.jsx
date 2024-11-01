// AllUsers.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdNavbar from './admin_navbar';

const AllUsers = () => {
    const accessToken = localStorage.getItem("accessToken");
    const [error , setError] = useState('');
    const [users , setUsers] = useState([]);
    let navigate = useNavigate(); // Use navigate instead of history

    useEffect(() => {
            const fetch_all_users = async () => {
                try {
                const response = await fetch(`http://127.0.0.1:8000/users_list`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log(data.users);
                setUsers(data.users);
                // setMessages(data.messages); // Update the messages state with fetched data
                // setMyId(data.id);
              
            } catch (error) {
                setError(error.message);
            }
            };
            fetch_all_users();
    }, []);

    const handleClick = (user) => {
        navigate(`/admin_user_view/${user}`)
    }

    return (
        <>
        <AdNavbar/>
        <div className="chat-sidebar">
            
            <h2>users</h2>
            {users && <ul>
                {users.map((user) => (
                    <li key={user.id} onClick={() => handleClick(user.id)}>
                        {user.name} , {user.email}
                    </li>
                ))}
            </ul>}
        </div>
        </>
    );
};

export default AllUsers;
