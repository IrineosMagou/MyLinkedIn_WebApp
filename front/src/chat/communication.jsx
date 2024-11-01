import React, { useState, useEffect, useCallback } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import CheckChat from './check';
import { useLocation, useParams } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import jwtDecode from 'jwt-decode';
import { Container, Typography } from '@mui/material';

const ChatComponent = () => {
    const location = useLocation();
    const { user_id } = location.state || {};
    const accessToken = localStorage.getItem("accessToken");
    const decodedToken = jwtDecode(accessToken);
    const { room_id } = useParams();
    const socketUrl = `ws://127.0.0.1:8000/ws?token=${encodeURIComponent(accessToken)}`;
    const [messageHistory, setMessageHistory] = useState([]);
    const [text, setText] = useState('');
    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
    const [receiver , setReceiver] = useState(user_id);
    const [chatId , setChatId] = useState(room_id);

    useEffect(() => {
        if (lastMessage !== null) {
            try {
                const messageData = JSON.parse(lastMessage.data);
                const messageWithId = {
                    id : uuidv4(),
                    sender : receiver,
                    content : messageData
                };
                setMessageHistory((prev) => [...prev, messageWithId]);
            } catch (error) {
                console.error('Failed to parse message:', lastMessage.data);
            }
        }
    }, [lastMessage, receiver]);

    const handleChange = (e) => {
        setText(e.target.value);
    };

    const handleSendMessage = useCallback(() => {
        const data = {
            chat_id: chatId,
            text: text,
            receiver_id: receiver
        };

        if (text.trim()) {
            const messageWithId = {
                id: uuidv4(),
                sender: Number(decodedToken.sub),
                content: text,
            };

            setMessageHistory((prev) => [...prev, messageWithId]);

            sendMessage(JSON.stringify({ data }));
            setText('');
        }
    }, [text, chatId, receiver, sendMessage]);

    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting...',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing...',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState];

    return (
        <Container>
            <CheckChat
                send={handleSendMessage}
                onChange={handleChange}
                text={text}
                setReceiver={setReceiver}
                history={messageHistory}
                NoRoom={chatId}
                setRoom={setChatId}
            />
            <Typography variant="body2">The WebSocket is currently {connectionStatus}</Typography>
            {lastMessage && <Typography variant="body2">Last Message: {lastMessage.data}</Typography>}
        </Container>
    );
};

export default ChatComponent;
