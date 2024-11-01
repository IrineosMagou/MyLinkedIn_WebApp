// ChatSidebar.js
import React, { useEffect, useState } from 'react';
import './sidebar.css'; // Import your CSS file for styling
import { Box, List, ListItem, ListItemText } from '@mui/material';

const ChatSidebar = ({  onSelectChat , setReceiver , room_id }) => {
    const accessToken = localStorage.getItem("accessToken");
    const [chats , setChats] = useState([])
    const [error , setError] = useState('');
    
    useEffect(() => {
        console.log(room_id);
        if(room_id){
            const fetch_chat_room = async () => {
                try {
                const response = await fetch(`http://127.0.0.1:8000/get_chat_info/${room_id}`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log(room_id);
                data['info']['chat_id'] = room_id
                onSelectChat(data.info)
             
            } catch (error) {
                setError(error.message);
            }
            };
            fetch_chat_room();
        }
        
            const fetch_chat_rooms = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:8000/get_user_chats`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` },
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    setChats(data.data);
                } catch (error) {
                    setError(error.message);
                } 
            };
            fetch_chat_rooms();  

    }, []);

    const handleClick = (chat) => {
        setReceiver(chat.user_id);
        onSelectChat(chat)
    }

    return (
        <div className="chat-sidebar">
            <h2>Chats</h2>
            {chats && <ul>
                {chats.map((chat) => (
                    <li key={chat.chat_id} onClick={() => handleClick(chat)}>
                        {chat.name}
                    </li>
                ))}
            </ul>}
        </div>
    );

};

export default ChatSidebar;


