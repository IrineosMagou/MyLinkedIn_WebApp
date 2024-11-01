import React, { useState } from 'react'
import { useAuth } from '../contextProvider';

const ChangeUsername = () => {
    const{setAccessToken} = useAuth();
    let data = '';
    let history = useNavigate();
    const [email , setEmail] = useState({});
    
    const [errorMessage,setErrorMessage] = useState('');
    const handleChange = (e) => {
      e.preventDefault();
      setEmail({...email , [e.target.name]: e.target.value})

    }
    const handleSubmit = async (e) => {
      e.preventDefault();
      const accessToken = localStorage.getItem('accessToken')
        try {
        const response =  await fetch('http://127.0.0.1:8000/change_email', {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json' ,
            'Authorization': `Bearer ${accessToken}`
          },
          body: JSON.stringify(email)
        })
            if (response.status === 200) {
                 data = await response.json();
                //  setSuccess(true)//so sign in page know what to display
                localStorage.removeItem('accessToken')
                setAccessToken(null);
                 history('/SignIn');//if the user is successfully created , go to sing in. then invoke 
            // Update state or perform other actions based on the successful response
          } else {
            console.log('mama');
            // Handle cases where redirected response is not OK
          }
        }
        catch (error) {
        console.error('Error:', error);
        }
    }
  return (
    <div>
      
      {errorMessage && 
        <h3 onClose={() => setErrorMessage("")} severity="error">
            {errorMessage}
        </h3>}
      <form action="submit" onSubmit={handleSubmit}>

      <label htmlFor="email" className='form-label'>
            Set new email
      </label>
          <input type="text" 
              className='form-input'
              id = 'email'
              name='email'
              value={email}
              onChange={handleChange}
          />
        <button className='btn'>Change</button>
      </form> 
    </div>
  )
}

export default ChangeUsername