import React, { useEffect, useState } from "react";
import { ProfileGrid } from "../Network/user_profile";
import { useNavigate } from "react-router-dom";
import { GridElem } from "../articles/article_fun";
import './notifications.css';


function Notifications () {
    const accessToken = localStorage.getItem('accessToken');
    const [requests , setRequests] = useState([]);
    const [articles , setArticles] = useState([]);
    const [loading , setLoading] = useState(null);
    const [error , setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/user_notifications`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                });
                if (response.status === 404) {
                    setError('Δεν υπάρχουν ειδοποιήσεις')
                }
                else if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                // setRequests(data.data);

                console.log(data);
                if (data != null){

                    setArticles(data.article_interactions);
                }
            } 
            catch (error) {
                setError(error.message);
            } 
            finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, []);

    if (loading) {return <p>Loading...</p>;}
    if (error) { return (<> <p>{error}</p>  </>);}
    
    const handleClick = (user_id) => {
        navigate(`/user_blog/${user_id}`)
    }
    const handleClick0 = (user_id) => {
        navigate(`/user_blog/${user_id}`)
    }
    return (
        <> 
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            <div className="notifications-container" style={{ display: 'flex' }}>
                <div style={{ flex: 1, padding: '10px' }}>
                    <h4>Αιτήματα Σύνδεσης :</h4>
                    {requests.map((user) => (
                        <ProfileGrid key={user.id} user={user} onClick={() => handleClick(user.id)} />
                    ))}
                </div>
                <div style={{ flex: 1, padding: '10px' }}>
    {articles && articles.length > 0 ? (
        <>
            <h4>Άρθρα:</h4>
            {articles.map((article) => (
                <GridElem
                    key={`${article.article_id}-${article.user_id}`}
                    article={article}
                    onClick={() => handleClick0(article.user_id)}
                />
            ))}
        </>
    ) : (
        <div>Δεν έχεις ειδοποίηση από άρθρο.</div>
    )}
</div>

            </div> 
        </>
    );

}
export default Notifications;
