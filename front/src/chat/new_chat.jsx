import {  useState } from "react"
import Button from "../myreuse/myButton"
import { useNavigate } from "react-router-dom";

const NewChat = ({user_id}) => {
    const accessToken = localStorage.getItem("accessToken");
    const [error , setError] = useState('')
    const navigate = useNavigate();

    const handleClick = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/chatroom/${user_id}`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                    const chat_room = data.chat_id
                    console.log(chat_room)
                    navigate(`/chat/${chat_room}` , { state: { user_id } });
            } catch (error) {
                setError(error.message);
            } 
    }

    if(error) {return(<p>{error}</p>)}
    return(
        <Button label="Συζήτηση" onClick={handleClick}/>
    )
  
}

export default NewChat