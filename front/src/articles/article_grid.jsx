import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Box, Typography, CircularProgress, Alert } from '@mui/material';
import { useAuth } from '../contextProvider';
import ArticleGrid from './article_fun';


function ConnectedArticles() {
  const navigate = useNavigate();
  const { setAccessToken } = useAuth(); 
  const [articles, setArticles] = useState({
    ArticleTitle: [],
    InterestArticle: [],
    Recommended: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const accessToken = localStorage.getItem('accessToken');

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/view_articles', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (!response.ok) {
          if (response.status === 401) {
            setAccessToken('');
            navigate('/SignIn');
          }
          if (response.status === 404) {
            throw new Error('Δεν υπάρχουν άρθρα.');
          }
        }

        const result = await response.json();
        console.log('API Response:', result);
        
        // Set individual categories of articles from the response
        setArticles({
          ArticleTitle: result.data.ArticleTitle || [],
          InterestArticle: result.data.InterestArticle || [],
          Recommended: result.data.Recommended || []
        });
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, [accessToken, navigate]);

  if (loading) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading articles...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      {/* Article Title Section */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Άρθρα Δικτύου</Typography>
        <Box sx={{ height: '200px', overflowY: 'auto', border: '1px solid #ccc', padding: 2 }}>
          <ArticleGrid articles={articles.ArticleTitle} />
        </Box>
      </Box>

      {/* Interest Article Section */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Στις Συνδέσεις σου Αρέσουν</Typography>
        <Box sx={{ height: '200px', overflowY: 'auto', border: '1px solid #ccc', padding: 2 }}>
          <ArticleGrid articles={articles.InterestArticle} />
        </Box>
      </Box>

      {/* Recommended Article Section */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>Προτεινόμενα </Typography>
        <Box sx={{ height: '200px', overflowY: 'auto', border: '1px solid #ccc', padding: 2 }}>
          <ArticleGrid articles={articles.Recommended} />
        </Box>
      </Box>
    </Container>
  );
}

export default ConnectedArticles;
