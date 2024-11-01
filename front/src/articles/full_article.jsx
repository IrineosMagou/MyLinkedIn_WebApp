import React, { useState, useEffect } from 'react';
import { ArticleView } from './article_fun';
import { useParams , useLocation } from 'react-router-dom';
import MediaViewer from './media_viewer';
import { DropText } from '../myreuse/drop_text';
import { Interest } from './article_fun';
import jwtDecode from 'jwt-decode';


function FullArticle() {
  const { article_id } = useParams();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [article, setArticle] = useState(location.state?.article || {});
  const [articleMedia , setArticleMedia] = useState([]);
  const accessToken = localStorage.getItem('accessToken');
  const [textAreaContent, setTextAreaContent] = useState('');
  const[myArticle , seMyArticle] = useState(null);
  let article_text ;

// =========================FOR_GRID_RENDERING=================================
// ============================================================================
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/full_article/${article_id}` ,
        {
            headers: {'Authorization': `Bearer ${accessToken}`}
        }); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data.data)

        if(data.data[0].media){  // If there is no media then the response structure is different
          setArticleMedia(data.data[0].media)
          article_text = data.data[0].article
        }
        else {
          article_text = data.data
           }
        setArticle(prevArticle => ({
        ...prevArticle,
        article : article_text // Merge existing article with new data
      }));
        console.log(article)
        
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
    const decodedToken = jwtDecode(accessToken);
    console.log(decodedToken.sub);
    console.log(article.id);
    if(decodedToken.sub == article.id){
      seMyArticle(true);
    }else{
      seMyArticle(false);  
    }
    
  console.log(myArticle);

  }, []);

  const handleComment = async () => {
    const toSend = {
      article_id :article_id ,
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
        console.log(data.Message)
        setTextAreaContent('');
    }catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
  }

  if (loading) return <p>Loading...</p>;
  // if (error) return <p>Error: {error}</p>;
  if (myArticle === null) {
    return <p>Loading...</p>;  // You can replace this with a loading spinner if needed
  }
  console.log(myArticle);
  // ====================================================================RETURN
  return (
    <>  
        
      <div className="article-grid">
        <ArticleView article = {article} />
     </div> 
        {articleMedia && (
           <div className="media-viewer-container">
             <MediaViewer fileUrls={articleMedia} art_id={article.art_id} />
           </div>
        )}
        {!myArticle && 
          <div> 
            <DropText textAreaContent={textAreaContent} setTextAreaContent={setTextAreaContent} onClick={handleComment}/> 
            <Interest article_id={article.art_id} friend_id={article.friend_id} interested={article.isInterest}/>
          </div>
        }
        

        
    </>
    
  );
}

export default FullArticle;
