import React, { useState, useCallback, useEffect } from 'react';
// import debounce from 'lodash.debounce';
import FileDropzone from '../myreuse/dropzone';
import Button from '../myreuse/myButton';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { Grid , Typography} from '@mui/material';

const ManageArticle = () => {
    const { article_id } = useParams();
    const location = useLocation();
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [article, setArticle] = useState(location.state?.article || {});
    const [articleMedia , setArticleMedia] = useState([]);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const[error , setError] = useState('');
    const [category, setCategory] = useState('');
    const[message , setMessage] = useState('');

    const accessToken = localStorage.getItem("accessToken");
    let article_text ;
const options = [
        'Technology',
        'Sports',
        'Business',
        'Health',
        'Design',
        'Art',
        'Science'
    ];
    const handleCategory = (event) => {
        setCategory(event.target.value); // Update the category state
    };

     useEffect(() => {
        const fetchArticles = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/full_article/${article_id}`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();


                if (data.data[0].media) { // If media is present in the response
                    setArticleMedia(data.data[0].media);
                    article_text = data.data[0].article;
                } else {
                    article_text = data.data;
                }
                // Update the article and title state
                setArticle(prevArticle => ({
                  ...prevArticle,
                  article: article_text
                }));
                
                setTitle(article.title);  // Set the title
                setText(article_text);    // Set the article text

            } catch (error) {
                setError(error.message);
            }
        };

        fetchArticles();
    }, [article_id, accessToken]); // Adding dependencies to avoid warnings


    const handleDrop = useCallback((acceptedFiles) => {
        setSelectedFiles(acceptedFiles);
    }, []);
    
  //  const handleChange = useCallback(
  //       debounce((e) => {
  //           e.preventDefault();

  //           const { name, value } = e.target;
  //           console.log(`Input changed: ${name} = ${value}`); // Debugging statement

  //           if (name === 'title') {
  //             console.log(e.target.value)
  //               setTitle( value );
  //           } else if (name === 'article') {
  //               setText(value);
  //           }
  //       }, 500), // Debounce delay
  //       []
  //   );
    const handleChange = (e) => {
      e.preventDefault();
      const { name, value } = e.target;
            console.log(`Input changed: ${name} = ${value}`); // Debugging statement
            if (name === 'title') {
                setTitle(value);
            } else if (name === 'article') {
                setText(value);
            }
    }

    const handleUpload = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        console.log(article_id);
        formData.append('id' , article_id);
        formData.append('title', title);
        formData.append('category', category);
        formData.append('article', text);

        for (const file of selectedFiles) {
            formData.append('media', file);
        }
        console.log(formData);
        try {
            const response = await fetch('http://127.0.0.1:8000/upload_article', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}` },
                body: formData,
            });
            if (response.ok) {
                console.log('Success:', response);
                setMessage("Επιτυχής Ανέβασμα");

            } else {
                console.error('Error:', response);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    console.log(article)

    return (
         <Grid container spacing={2}>
            {/* Form Grid */}
            <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                   Επεξεργασία Άρθρου
                </Typography>
            {message && <p>{message}</p>}

                <form className='form' onSubmit={handleUpload}>
                    <textarea
                        id='title'
                        name='title'
                        value={title}
                        onChange={handleChange}
                        style={{ width: '100%' , fontSize: '16px' }}
                        placeholder="Write your title here..."
                    />
                    <textarea
                        id='article'
                        name='article'
                        value={text}
                        onChange={handleChange}
                        style={textareaStyles}
                        placeholder="Write your article here..."
                    />
                    <FileDropzone onDrop={handleDrop} />
                    <Button label="Ανέβασε το άρθρο" type='submit' />
                    <label htmlFor="category">Select a Category:</label>
                        <select id="category" value={category} onChange={handleCategory}>
                            <option value="" disabled>Select a category</option>
                            {options.map((option, index) => (
                                <option key={index} value={option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                </form>
            </Grid>
        </Grid>
    );
};

const textareaStyles = {
    width: '100%',
    maxWidth: '1200px',
    height: '600px',
    fontSize: '16px',
    padding: '20px',
    border: '2px solid #cccccc',
    borderRadius: '4px',
    boxSizing: 'border-box',
    resize: 'none',
    overflow: 'auto',
};

export default ManageArticle;
