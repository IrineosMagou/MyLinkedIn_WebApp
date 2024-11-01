import React, { useState } from 'react';
import { Grid , Typography} from '@mui/material';
import MyArticles from './my_articles';
import FileDropzone from '../myreuse/dropzone';
import Button from '../myreuse/myButton';

const UploadArticle = () => {
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [category, setCategory] = useState('');
    const [selectedFiles, setSelectedFiles] = useState([]);
    const[message , setMessage] = useState('');
    const accessToken = localStorage.getItem("accessToken");
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
    const handleDrop = (acceptedFiles) => {
        setSelectedFiles(acceptedFiles);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'title') {
            setTitle(value);
        } else if (name === 'article') {
            setText(value);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        console.log(typeof category);
        console.log(typeof title);
        console.log(typeof text);
        const formData = new FormData();
        formData.append('title', title);
        console.log(title);
        console.log(category);
        formData.append('category', category);
        formData.append('article', text);
        
        for (const file of selectedFiles) {
            formData.append('media', file);
        }
        for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }
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

    return (
        <Grid container spacing={2}>
            {/* Articles Grid */}
            <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                    Επεξεργασία Άρθρου
                </Typography>
                <MyArticles />
            </Grid>

            {/* Form Grid */}
            {message && <p>{message}</p>}
            <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                   Ανέβασε Άρθρο
                </Typography>
                <form className='form' onSubmit={handleUpload}>
                    <textarea
                        id='title'
                        name='title'
                        value={title}
                        onChange={handleChange}
                        style={{ width: '100%' }}
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
                    <label htmlFor="category">Select a Category:</label>
                        <select id="category" value={category} onChange={handleCategory}>
                            <option value="" disabled>Select a category</option>
                            {options.map((option, index) => (
                                <option key={index} value={option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                {category && <p>You selected: {category}</p>}                
                <Button label="Ανέβασε το άρθρο" type='submit' />
            </form>
            </Grid>
        </Grid>
    );
};

const textareaStyles = {
    width: '100%',
    height: '400px',
    fontSize: '16px',
    padding: '10px',
    border: '1px solid #cccccc',
    borderRadius: '4px',
    boxSizing: 'border-box',
    resize: 'none',
    overflow: 'auto',
};

export default UploadArticle;
