import React, { useState, useEffect } from 'react';
import AdGrid from './ads_fun';
import { Link } from 'react-router-dom';
import Button from '../myreuse/myButton';

function ConnectedAds() {
  const [myAds, setMyAds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const accessToken = localStorage.getItem('accessToken');

// =========================FOR_GRID_RENDERING=================================
  useEffect(() => {
    const fetchAds = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/view_ads' , {
          headers: {'Authorization': `Bearer ${accessToken}`}
        }); 
        console.log(response);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMyAds(data.data);
        console.log(data.data)
        console.log(myAds)    
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAds();
  }, []);

  if (loading) return <p>Loading...</p>;
  // if (error) return <p>Error: {error}</p>;

  // ====================================================================RETURN
  return (
      <div className="ads-grid">
        <AdGrid ads = {myAds} />
        <Link to="/upload_ad">
          <Button label="Ανέβασε Αγγελία" />
        </Link>
     </div> 
  );
}

export default ConnectedAds;