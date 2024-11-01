import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contextProvider';
import Button from '../myreuse/myButton';
import ProfilePicture from './insert_pictures';
import jwtDecode from 'jwt-decode';

const SignUp = () => {
  let history = useNavigate();
  const { setAccessToken , setIdPic } = useAuth(); 
  const [password0, setPassword0] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [user, setUser] = useState({
    name: '',
    surname: '',
    password: '',
    email: '',
    phone: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name !== 'password0') {
      setUser({ ...user, [name]: value });
    } else {
      setPassword0(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const emptyProps = Object.keys(user).filter(prop => user[prop] === '');
    if (emptyProps.length > 0) {
      setErrorMessage('Please fill all the blanks');
      return;
    }
    if (user.password.length < 8) {
      setErrorMessage('Password must be at least 8 characters');
      return;
    }
    if (user.password !== password0) {
      setErrorMessage('Passwords do not match');
      return;
    }

    const formData = new FormData();
    formData.append('name', user.name);
    formData.append('surname', user.surname);
    formData.append('password', user.password);
    formData.append('email', user.email);
    formData.append('phone', user.phone);

    if (selectedFiles) {
      formData.append('picture', selectedFiles);
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/create_user/', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        const decodedToken = jwtDecode(token);
        setIdPic(decodedToken.sub);
        localStorage.setItem('accessToken', token);
        localStorage.setItem('id', decodedToken.sub);
        setAccessToken(token);
        history("/personal_info");
      } else {
        const data = await response.json();
        setErrorMessage(data ? 'Email already exists' : 'An error occurred');      }
    } catch (error) {
      setErrorMessage('An unexpected error occurred');
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form className='form' onSubmit={handleSubmit} id='registration-form'>
        <h4>Δημιουργία Λογαριασμού</h4>
        <div className='form-row'>
          <label htmlFor='name' className='form-label'>Όνομα</label>
          <input
            type='text'
            className='form-input'
            id='name'
            name='name'
            value={user.name}
            onChange={handleChange}
          />
        </div>
        <div className='form-row'>
          <label htmlFor='surname' className='form-label'>Επίθετο</label>
          <input
            type='text'
            className='form-input'
            id='surname'
            name='surname'
            value={user.surname}
            onChange={handleChange}
          />
        </div>
        <div className='form-row'>
          <label htmlFor='password' className='form-label'>Κωδικός</label>
          <input
            type='password'
            className='form-input'
            id='password'
            name='password'
            value={user.password}
            onChange={handleChange}
          />
        </div>
        <div className='form-row'>
          <label htmlFor='password0' className='form-label'>Επιβεβαίωση Κωδικού</label>
          <input
            type='password'
            className='form-input'
            id='password0'
            name='password0'
            value={password0}
            onChange={handleChange}
          />
        </div>
        <div className='form-row'>
          <label htmlFor='email' className='form-label'>Email</label>
          <input
            type='email'
            className='form-input'
            id='email'
            name='email'
            value={user.email}
            onChange={handleChange}
          />
        </div>
        <div className='form-row'>
          <label htmlFor="phone" className='form-label'>Τηλέφωνο Επικοινωνίας</label>
          <input
            type="tel"
            className='form-input'
            id="phone"
            name="phone"
            value={user.phone}
            onChange={handleChange}
          />
        </div>
        <ProfilePicture selectedFile={selectedFiles} setSelectedFile={setSelectedFiles}/>
        <Button type='submit' label="Εγγραφή" />
        {errorMessage && <h4>{errorMessage}</h4>}
      </form>

    </div>
  );
};

export default SignUp;
