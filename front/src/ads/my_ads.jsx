import React , { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const MyAds = () => {
    let navigate = useNavigate();
    const [myAds , setMyAds] = useState([]);
    const [error , setError] = useState('');
    const accessToken = localStorage.getItem("accessToken");
    useEffect(() => {
        const fetchArticles = async () => {
          try {
            const response = await fetch('http://127.0.0.1:8000/get_my_ads' , {
              headers: {'Authorization': `Bearer ${accessToken}`}
            }); 
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setMyAds(data.data);
            console.log(data.data);
          } catch (error) {
            setError(error.message);
          }
        };
        fetchArticles();
    },[]);

    const handleClick = (ad) => {
        navigate(`/ad_manage/${ad.id}`, { state: { ad } });
    };

    return(
        <>
            <div className="category-grid">
    {myAds && myAds.length > 0 ? (
      myAds.map((ad, index) => (
        <div key={index} className="grid-item" onClick={() => handleClick(ad)}>
          {ad.title}
        </div>
      ))
    ) : (
      <div>Δεν έχεις ακόμη ανεβάσει αγγελία.</div> // Fallback UI if there are no articles
    )}
  </div>
        </>
    )
}

export default MyAds