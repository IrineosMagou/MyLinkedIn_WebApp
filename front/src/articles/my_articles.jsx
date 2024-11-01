import React , { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const MyArticles = () => {
    let navigate = useNavigate();
    const [myArticles , setMyArticles] = useState([]);
    const [error , setError] = useState('');
    const accessToken = localStorage.getItem("accessToken");
    useEffect(() => {
        const fetchArticles = async () => {
          try {
            const response = await fetch('http://127.0.0.1:8000/get_my_articles' , {
              headers: {'Authorization': `Bearer ${accessToken}`}
            }); 
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setMyArticles(data.data);
            console.log(data.data);
          } catch (error) {
            setError(error.message);
          }
        };
        fetchArticles();
    },[]);

    const handleClick = (article) => {
        console.log(article.id)
        navigate(`/article_manage/${article.id}`, { state: { article } });
    };

    return(
        <>
  <div className="category-grid">
    {myArticles && myArticles.length > 0 ? (
      myArticles.map((article, index) => (
        <div key={index} className="grid-item" onClick={() => handleClick(article)}>
          {article.title}
        </div>
      ))
    ) : (
      <div>Δεν έχεις ακόμη ανεβάσει άρθρο.</div> // Fallback UI if there are no articles
    )}
  </div>
</>

    )
}

export default MyArticles