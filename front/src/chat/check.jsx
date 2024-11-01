import { useEffect, useRef, useState } from 'react';
import ChatSidebar from './sidebar';
import ChatWindow from './window';
import { Link } from 'react-router-dom';
import Button from '../myreuse/myButton';
import { Box , Button as MUIbutton} from '@mui/material';


const CheckChat = ({ send, onChange, text, setReceiver, history, NoRoom , setRoom}) => {
    const accessToken = localStorage.getItem("accessToken");
    const [selectedChat, setSelectedChat] = useState(null);
    const [messages, setMessages] = useState([]);
    const [error, setError] = useState('');
    const [combinedMessages, setCombinedMessages] = useState([]);
    const [myId, setMyId] = useState(null);
    // const [roomId, setRoomId] = useState('');
    // const [sidebarVisible, setSidebarVisible] = useState(false);
    const prevHistoryRef = useRef();

    // Fetch chat messages by room ID
    const fetchChat = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/get_chat_messages/${id}`, {
                headers: { 'Authorization': `Bearer ${accessToken}` },
            });
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            setMessages(data.messages);
            setMyId(data.id);
            console.log(data);

        } catch (error) {
            setError(error.message);
        }
    };

    // Fetch the last active chat if NoRoom is not provided
    useEffect(() => {
        if (NoRoom === undefined) {
            const fetchLastChat = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:8000/get_last_chat`, {
                        headers: { 'Authorization': `Bearer ${accessToken}` },
                    });
                    if (!response.ok) throw new Error('Network response was not ok');
                    
                    const data = await response.json();
                    const lastRoomId = data.info.last_chat;
                    console.log(data);
                    setReceiver(data.info.other_user);
                    fetchChat(lastRoomId);
                    setRoom(lastRoomId);
                } catch (error) {
                    setError(error.message);
                }
            };

            fetchLastChat();
        } else {
            console.log(NoRoom);
            fetchChat(NoRoom);
            setRoom(NoRoom);
        }
    }, [NoRoom]);

    // Combine history and messages
    useEffect(() => {
    //     console.log(history);
    //     console.log(messages);
    if (history.length === 0) {
        setCombinedMessages(messages);
    } else {
        const prevHistory = prevHistoryRef.current;

        if (JSON.stringify(prevHistory) !== JSON.stringify(history)) {
            setCombinedMessages([...messages, ...history]);
        } else {
            setCombinedMessages([...messages]);
        }
    }
    prevHistoryRef.current = history;
}, [history, messages]);


    // Handle selecting a chat
    const handleSelectChat = async (chat) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/get_chat_messages/${chat.chat_id}`, {
                headers: { 'Authorization': `Bearer ${accessToken}` },
            });
            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            setMessages(data.messages);
            setMyId(data.id);
        } catch (error) {
            setError(error.message);
        }
        setSelectedChat(chat);
    };

    // Add new message to the messages state
    const addMessage = (newMessage) => {
        setCombinedMessages((prevMessages) => [...prevMessages, newMessage]);
    };
        console.log(combinedMessages);

    // const handleToggleSidebar = () => {
    //     setSidebarVisible((prev) => !prev);
    // };
    return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
        {error && (
            <div className="error-message">
                <Link to='/network'>
                    <Button label='Συνδέσου με Χρήστες' />
                </Link>
            </div>
        )}

        {NoRoom && (
            <ChatSidebar onSelectChat={handleSelectChat} setReceiver={setReceiver} room_id={NoRoom} />
        )}

        <Box sx={{ flexGrow: 1, p: 2, marginLeft: NoRoom ? '250px' : '0' }}>
            <ChatWindow
                selectedChat={selectedChat}
                setSelectedChat={setSelectedChat}
                onClick={send}
                text={text}
                onChange={onChange}
                toRender={combinedMessages} // Pass combined messages
                addMessage={addMessage}
                myId={myId}
            />
        </Box>
    </Box>
);




};
 
export default CheckChat;