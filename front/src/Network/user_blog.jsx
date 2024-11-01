import React, { useEffect, useState } from "react";
import { UserProfile } from "./user_profile";
import { useParams , Link } from "react-router-dom";
import Button from "../myreuse/myButton";
import NewChat from "../chat/new_chat";
import jwtDecode from 'jwt-decode';


function UserBlog() {
    const { user_id } = useParams();
    const accessToken = localStorage.getItem('accessToken');
    const [user, setUser] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message , setMessage] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);
    const [myProfile , setMyProfile] = useState(false);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/user_view/${user_id}`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setUser(data.data);
                const decodedToken = jwtDecode(accessToken);
                const admin = decodedToken.scopes;
                console.log(data.data);
                if (admin.length === 2) {
                    setIsAdmin(true); // Use setIsAdmin to update the state
                } else if(decodedToken.sub === user_id) {
                    setMyProfile(true);
                }

            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, [message]);

    const handleClick = async (action) => {
        setLoading(true);
        let toSend = {}; 
        let endpoint = '';
        if(action == 'REQUEST'){
            toSend = {
                id     : user_id
            }
            endpoint = 'http://127.0.0.1:8000/connection_request'
        }
        else{
            toSend = {
                handle : action , 
                id : user_id
            }
            endpoint = 'http://127.0.0.1:8000/handle_request'
        }
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                mode: 'cors',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(toSend),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setMessage(data.Message);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (isAdmin ) return <div><UserProfile user = {user.data}/></div>
    if(myProfile)return(
        <div>
            <UserProfile user = {user.data}/> 
            <Link to = '/account_settings'>
                <Button label= "Επεξεργασία στοιχείων " />
            </Link>
        </div>
    ) 
        
    // if (message) return <p>message: {message}</p>;
    return (
        <>
            <UserProfile user={user.data} />
            {!user.data.connection_status ?
                (<Button label="Αίτημα Σύνδεσης" onClick={ () => handleClick('REQUEST')} disabled={loading} />)
                :(
                    user.data.connection_status == "Accepted"  ? (
                        <>
                        <Button label="Διαγραφή Σύνδεσης" onClick={ () => handleClick('CANCEL')} disabled={loading} />
                        <NewChat user_id={user.data.id}/>
                        </>
                    ):( 

                    user.data.sender === 1 ? 
                    ( <Button label= "ΑΚΥΡΩΣΗ " onClick={ () => handleClick('CANCEL')} disabled={loading} />  ) 
                :(
                    <> 
                    <Button label= "Αποδοχή " onClick={ () => handleClick('ACCEPT')} disabled={loading} />
                    <Button label= "Απόρριψη " onClick={( ) => handleClick('REJECT')} disabled={loading} />
                    </>                
                )         
            ))}
            {message && <h3>{message}</h3>}
        </>
    );
}

export default UserBlog;
