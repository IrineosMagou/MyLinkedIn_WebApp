import React from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';

const ChatWindow = ({ selectedChat, text, onChange, onClick, toRender, addMessage, myId }) => {

    const renderFetchedMessages = () => {
        const uniqueMessages = [...new Map(toRender.map(msg => [msg.id, msg])).values()];
        return uniqueMessages.map((message) => (
            <Box key={message.id} className="message" sx={{ mb: 1 }}>
                <Typography variant="body2" sx={{ fontWeight: message.sender === myId ? 'bold' : 'normal' }}>
                    {message.sender === myId ? 'You' : `User ${message.sender}`}: {message.content}
                </Typography>
            </Box>
        ));
    };

    const handleMessageInput = () => {
        const newMessageObject = {
            id: uuidv4(),
            sender: myId,
            content: text,
        };
        onClick();
        addMessage(newMessageObject);
    };

    if (!selectedChat) {
        return <Typography variant="h6">Select a chat to start messaging</Typography>;
    }

    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>{selectedChat.name}</Typography>
            <Box
                className="messages-container"
                sx={{
                    height: 400, // Fixed height
                    overflowY: 'scroll', // Scrollable when content exceeds
                    border: '1px solid #ccc',
                    p: 2,
                    mb: 2
                }}
            >
                {renderFetchedMessages()}
            </Box>
            <TextField
                id="message"
                name="message"
                value={text}
                onChange={onChange}
                fullWidth
                placeholder="Type a message..."
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        handleMessageInput();
                    }
                }}
                sx={{ mb: 2 }}
            />
            <Button variant="contained" onClick={handleMessageInput}>
                Send
            </Button>
        </Box>
    );
};

export default ChatWindow;
