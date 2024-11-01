import React, { useState, useEffect } from 'react';
import { useParams , useLocation } from 'react-router-dom';
import { AdView } from './ads_fun';
import { DropText } from '../myreuse/drop_text';
import { Interest } from './ads_fun';
import jwtDecode from 'jwt-decode';

function FullAd() {
  const { ad_id } = useParams();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [ad, setAd] = useState(location.state?.ad || {});
  const accessToken = localStorage.getItem('accessToken');
  const [textAreaContent, setTextAreaContent] = useState('');
  const [ myAd , setMyAd] = useState(null);
  let article_text ;
// =========================FOR_GRID_RENDERING=================================
// ============================================================================
  useEffect(() => {
    const fetchAd = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/full_ad/${ad_id}` ,
        {
            headers: {'Authorization': `Bearer ${accessToken}`}
        }); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data.data)

        setAd(prevAd => ({
        ...prevAd,
        ad : data.data.ad // Merge existing ad with new data
      }));
        
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAd();
    const decodedToken = jwtDecode(accessToken);
    // console.log(decodedToken.sub);
    // console.log(ad.id);
    if(decodedToken.sub == ad.id){
      setMyAd(true);
    }else{
      setMyAd(false);  
    }
  }, []);

  const handleComment = async () => {
    const toSend = {
      ad_id :ad_id ,
      comment : textAreaContent
    };
    // console.log(data);
    try {
        const response = await fetch(`http://127.0.0.1:8000/comment_article` ,
        {
          method : "POST"  ,
          headers: {'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json',},
          body: JSON.stringify(toSend), 

        }); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // console.log(data.Message)
        setTextAreaContent('');
    }catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
  }

  if (loading) return <p>Loading...</p>;
  // if (error) return <p>Error: {error}</p>;
  console.log(ad)

  // ====================================================================RETURN
  return (
    <>  
        
      <div className="ad-grid">
        <AdView ad = {ad} />
     </div> 
        {!myAd &&
          <div> 
            <DropText textAreaContent={textAreaContent} setTextAreaContent={setTextAreaContent} onClick={handleComment}/> 
            <Interest ad_id={ad.ad_id} friend_id={ad.friend_id} interested={ad.isInterest}/>
          </div>
        }

        
    </>
    
  );
}

export default FullAd;
