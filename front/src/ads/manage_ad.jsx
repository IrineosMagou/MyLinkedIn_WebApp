import React, { useState, useCallback, useEffect } from 'react';
// import debounce from 'lodash.debounce';
import Button from '../myreuse/myButton';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { Grid , Typography} from '@mui/material';

const ManageAd = () => {
    const { ad_id } = useParams();
    const location = useLocation();
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [ad, setAd] = useState(location.state?.ad || {});
    const[error , setError] = useState('');
    const accessToken = localStorage.getItem("accessToken");
    let ad_text , ad_title ;

     useEffect(() => {
        const fetchAd = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/full_ad/${ad_id}`, {
                    headers: { 'Authorization': `Bearer ${accessToken}` }
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                ad_text = data.data.ad;
                console.log(data.data.ad);
                setAd(prevAd => ({
                  ...prevAd,
                  ad: ad_text
                }));
                
                setTitle(ad.title);  // Set the title
                setText(ad_text);    // Set the article text

            } catch (error) {
                setError(error.message);
            }
        };

        fetchAd();
    }, [ad_id, accessToken]); // Adding dependencies to avoid warnings


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
            text : text ,
            id   : ad_id
        }
        try {
            const response = await fetch('http://127.0.0.1:8000/upload_ad', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${accessToken}` ,
                            'Content-Type': 'application/json' },
                body: JSON.stringify(toSend),
            });
            if (response.ok) {
                console.log('Success:', response);
            } else {
                console.error('Error:', response);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    console.log(ad)

    return (
         <Grid container spacing={2}>
            {/* Form Grid */}
            <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                   Επεξεργασία Άρθρου
                </Typography>
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
                        id='ad'
                        name='ad'
                        value={text}
                        onChange={handleChange}
                        style={textareaStyles}
                        placeholder="Write your ad here..."
                    />
                    <Button label="Ανέβασε το άρθρο" type='submit' />
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

export default ManageAd;
