// src/UserGrid.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ad_custom.css'
import Button from '../myreuse/myButton';
import { Link } from 'react-router-dom';
import jwtDecode from 'jwt-decode';
import { useAuth } from '../contextProvider';


// Profile on the Grid Component
export function GridElem({ ad , onClick}) {
  const { accessToken} = useAuth(); 
  const decodedToken = jwtDecode(accessToken);
  return (
    <>
      <div className="user-ads" onClick={onClick}>     
        <h4>{ad.title}</h4>
        <p> {ad.name} {ad.surname}</p>
      </div>
      {decodedToken.sub != ad.uploader &&

        <Interest ad_id={ad.ad_id} friend_id={ad.friend_id} interested={ad.isInterest}/>
      }
    </>
  );
}

export function AdView({ ad }) {
  return (
<div className="ad_read" >     
      <h3>Τίτλος : {ad.title}</h3>
      <p>{ad.ad}</p>
      <>
      <Link to= {`/user_blog/${ad.uploader}`}>
          <div>
          <p>Ανέβηκε από :</p>
          <Button label={`${ad.name} ${ad.surname}`} />
          </div>
      </Link>
      </>
      
    </div>
  );
}

// Article Grid Component
const AdGrid = ({ ads }) => {
  const navigate = useNavigate();
  const categoryLabels = {
  ArticleTitle: '',
  InterestArticle: 'Στις συνδέσεις σου αρέσουν'
};
  const handleClick = (ad) => {
    navigate(`/read_ad/${ad.ad_id}`, { state: { ad } });
  };
  // console.log(ads)
  if (!ads || ads.length === 0) return <p>Δεν υπάρχουν διαθέσιμες αγγελίες για προβολή.</p>;  // Display this message if no articles are present

  return (
    <div className="article-grid">
      {Object.entries(ads).map(([category, categoryAds]) => (
        <div key={category} className="category-section">
          <h3>{categoryLabels[category] || category}</h3>
          <div className="category-grid">
            {categoryAds.map((ad, index) => (
              <div key={index} className="grid-item">
                <GridElem ad={ad} onClick={() => handleClick(ad)} />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AdGrid;


export function Interest({ ad_id, friend_id, interested }) {
  const accessToken = localStorage.getItem('accessToken');
  const [checked, setChecked] = useState(interested); // Initialize with the boolean value

  const handleCheck =  async (e) => {
    e.preventDefault(); // Prevent default behavior
    let toSend = {}; 
    if(e.target.name == 'interest')
        toSend = {
                id : ad_id ,
                interest : true
            }
    else{
      toSend = {
                id : ad_id ,
                interest : false
            }
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/ad_interest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Ensure content type is set to JSON
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(toSend), // Send integer ID in the request body       
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setChecked(!checked); // Toggle the checked state
    } catch (error) {
      console.error('Error:', error);
    } 
  };

  return (
    <>
      {checked === false ? (
        <>
          <label>
            Ενδιαφέρον
            <input 
              type="checkbox" 
              name='interest'
              checked={checked} 
              onChange={handleCheck} 
            />
          </label>
          {friend_id && <p>{friend_id} is interested</p>}
        </>
      ) : (
        <label>
            Όχι Ενδιαφέρον
            <input 
              type="checkbox" 
              name='not_interest'
              checked={!checked} 
              onChange={handleCheck} 
            />
          </label>      )}
    </>
  );
}
