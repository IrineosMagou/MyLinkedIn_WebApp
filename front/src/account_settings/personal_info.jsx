import React, { useState, useEffect } from 'react';
import { Container, Box, Typography, TextField, Button, FormControlLabel } from '@mui/material';

const PersonalInfoForm = () => {
  const accessToken = localStorage.getItem("accessToken");
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [formData, setFormData] = useState({
    profession: '',
    age: '',
    experience: '',
    education: '',
    skills: '',
    employment: '',
    is_employment_p: false,
    is_age_p: false,
    is_experience_p: false,
    is_education_p: false,
    is_skills_p: false,
  });

  // Fetch personal info and populate the form
  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get_personal_info', {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const personalInfo = data.info;
        console.log(data);
        if(personalInfo){
          setFormData({
          profession: personalInfo[1] ?? '',
          age: personalInfo[2] ?? '',
          experience: personalInfo[3] ?? '',
          education: personalInfo[4] ?? '',
          skills: personalInfo[5] ?? '',
          employment: personalInfo[6] ?? '',
          is_age_p: Boolean(personalInfo[7]),
          is_experience_p: Boolean(personalInfo[8]),
          is_education_p: Boolean(personalInfo[9]),
          is_skills_p: Boolean(personalInfo[10]),
          is_employment_p: Boolean(personalInfo[11]),
        });
      }
        
      } catch (error) {
        setError(error.message);
        console.log(error);

      }
    };
    fetchInfo();
  }, [accessToken]); // Only runs when accessToken changes

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/personal-info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        const data = await response.json();
        setError(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4, mb: 4, padding: 3, backgroundColor: '#f9f9f9', borderRadius: 2, boxShadow: 2 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Personal Info
        </Typography>
        <form onSubmit={handleSubmit}>
          <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            label="Profession"
            name="profession" // Add the new field name
            value={formData.profession} // Bind the value to formData
            onChange={handleChange} // Use the same change handler
            placeholder="Enter your LinkedIn Profile URL"
            variant="outlined"
          />
        </Box>
          {['age', 'experience', 'employment', 'education', 'skills'].map((field, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <TextField
                fullWidth
                label={field.charAt(0).toUpperCase() + field.slice(1)}
                name={field}
                value={formData[field]} // Bind the value to formData
                onChange={handleChange}
                placeholder={`Enter your ${field}`} // Placeholder is shown only if value is ''
                variant="outlined"
              />
              <FormControlLabel
                control={
                  <input
                    type="checkbox"
                    name={`is_${field}_p`}
                    checked={formData[`is_${field}_p`]} // Checkbox value bound to formData
                    onChange={handleChange}
                  />
                }
                label={`Make ${field.charAt(0).toUpperCase() + field.slice(1)} Private`}
              />
            </Box>
          ))}
          <Button variant="contained" color="primary" type="submit" fullWidth>
            Submit
          </Button>
          {message && <Typography color="green">{message}</Typography>}
          {error && <Typography color="red">{error}</Typography>}
        </form>
      </Box>
    </Container>
  );
};

export default PersonalInfoForm;
