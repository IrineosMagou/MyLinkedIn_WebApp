import React, { useEffect, useState } from "react";
import { UserProfile } from "../Network/user_profile";
import { useParams } from "react-router-dom";
import Button from "../myreuse/myButton";
import AdNavbar from "./admin_navbar";

function UserView() {
    const { user_id } = useParams();
    const accessToken = localStorage.getItem('accessToken');
    const [user, setUser] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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
                console.log(data.data);
                setUser(data.data); 
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, [user_id, accessToken]);

    const handleDownloadJSON = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/user_data/${user_id}`, {
                headers: { 'Authorization': `Bearer ${accessToken}` },
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data.user);
            setUser((prevUser) => ({
                ...prevUser,
                ...data.user
            }));

            const blob = new Blob([JSON.stringify({ ...user, ...data.user }, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'user_data.json';
            link.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadXML = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/user_data/xml/${user_id}`, {
            headers: { 
                'Authorization': `Bearer ${accessToken}`
            },
        });

        const responseText = await response.text(); // Get the response as text
        console.log("Response Text:", responseText); // Log the raw response for debugging

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const xmlData = responseText; 
        const blob = new Blob([xmlData], { type: 'application/xml' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'user_data.xml'; // Name of the XML file
        link.click();
        URL.revokeObjectURL(url);
    } catch (error) {
        setError(error.message);
    } finally {
        setLoading(false);
    }
};




    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <>
            <AdNavbar/>
            <UserProfile user={user.data} />
            <Button label='Download JSON' onClick={handleDownloadJSON} />
            <Button label='Download XML' onClick={handleDownloadXML} />
        </>
    );
}

export default UserView;
