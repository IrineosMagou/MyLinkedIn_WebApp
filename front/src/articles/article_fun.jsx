// src/UserGrid.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './article_custom.css';
import Button from '../myreuse/myButton';
import { Link } from 'react-router-dom';
import jwtDecode from 'jwt-decode';
import { useAuth } from '../contextProvider';
import { Box, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

// Profile on the Grid Component
export function GridElem({ article , onClick}) {
  const { accessToken} = useAuth(); 
  const decodedToken = jwtDecode(accessToken);
  console.log(article.uploader);
  return (
    <>
      <div className="user-articles" onClick={onClick}>     
        <h4>{article.title}</h4>
        <p> {article.name} {article.surname}</p>
        <p>{article.category_name}</p>
      </div>
        {decodedToken.sub != article.uploader &&
        <Interest article_id={article.art_id} friend_id={article.friend_id} interested={article.isInterest}/>
        }
    </>
  );
}

export function ArticleView({ article }) {
  
  return (
<div className="article_read" >     
      <h3>Τίτλος : {article.title}</h3>
      <p>Είδος : {article.category_name}</p>
      <p>{article.article}</p>
      <>
      <Link to= {`/user_blog/${article.uploader}`}>
          <div>
          <p>Ανέβηκε από :</p>
          <Button label={`${article.name} ${article.surname}`} />
          </div>
      </Link>
      </>
      
    </div>
  );
}

const ArticleGrid = ({ articles }) => {
  const navigate = useNavigate();
  const handleClick = (article) => {
    console.log(article.art_id);
    navigate(`/read_article/${article.art_id}`, { state: { article } });
  };

  return (
  <Box>
    {/* Article Titles Section */}
    {articles.length > 0 && (
      <Box sx={{ mb: 4 }}>
        {/* <Typography variant="h6" sx={{ mb: 2 }}>Articles</Typography> */}
        <Box sx={{ height: '150px', overflowY: 'auto', border: '1px solid #ccc', padding: 2 }}>
          {articles.map((article, index) => (
            <Box key={index} sx={{ mb: 1 }}>
              <Typography variant="body1" onClick={() =>  handleClick(article)} sx={{ cursor: 'pointer' }}>
                {article.title}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {`By: ${article.name} ${article.surname}`}
              </Typography>
              <Divider sx={{ my: 1 }} />
              
            </Box>
          ))}
        </Box>
      </Box>
    )}
  </Box>
);

};

export default ArticleGrid;






export function Interest({ article_id, friend_id, interested }) {
  const accessToken = localStorage.getItem('accessToken');
  const [checked, setChecked] = useState(interested); // Initialize with the boolean value

  const handleCheck =  async (e) => {
    e.preventDefault(); // Prevent default behavior
    let toSend = {}; 
    if(e.target.name == 'interest')
        toSend = {
                id : article_id ,
                interest : true
            }
    else{
      toSend = {
                id : article_id ,
                interest : false
            }
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/article_interest', {
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
