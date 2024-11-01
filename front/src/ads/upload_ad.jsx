import React, { useState, useCallback } from 'react';
import debounce from 'lodash.debounce';
import Button from '../myreuse/myButton';
import { Grid , Typography} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import MyAds from './my_ads';
const UploadAd = () => {
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const accessToken = localStorage.getItem("accessToken");
    const navigate = useNavigate();

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
            } else if (name === 'ad') {
                setText(value);
            }
    }

    const handleUpload = async (e) => {
        e.preventDefault();
        const toSend = {
            title : title ,
            text : text
        };
        console.log(toSend);
        try {
            const response = await fetch('http://127.0.0.1:8000/upload_ad', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}` ,
                            'Content-Type': 'application/json' },
                body: JSON.stringify(toSend),
            });

            if (response.ok) {
                console.log('Success:', response);
                navigate("/");
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
                    Επεξεργασία Aγγελίας
                </Typography>
                <MyAds />
            </Grid>

            {/* Form Grid */}
            <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                   Ανέβασε Αγγελία
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
                        id='ad'
                        name='ad'
                        value={text}
                        onChange={handleChange}
                        style={textareaStyles}
                        placeholder="Write your ad here..."
                    />
                    <Button label="Ανέβασε την αγγελία" type='submit' />
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

export default UploadAd;
