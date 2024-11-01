import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Box, Typography } from '@mui/material';
import Button from '../myreuse/myButton';

const SettingsOptions = () => {
  return (
    <Container maxWidth="sm" sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
      {/* Title */}
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 4 }}>
       ΔΙΑΧΕΙΡΙΣΗ ΛΟΓΑΡΙΑΣΜΟΥ
      </Typography>

      {/* Options */}
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Link to="/change_password" style={{ textDecoration: 'none', marginBottom: '16px' }}>
          <Button
            colorScheme="BlackAlpha.800"
            variant="link"
            style={{ marginRight: '7px' }}
            label="Αλλαγη Κωδικου"
          />
        </Link>
        <Link to="/change_username" style={{ textDecoration: 'none', marginBottom: '16px' }}>
          <Button
            colorScheme="BlackAlpha.800"
            variant="link"
            style={{ marginRight: '7px' }}
            label="Αλλαγη Ηλ.Ταχυδρομειου"
          />
        </Link>
        <Link to="/personal_info" style={{ textDecoration: 'none', marginBottom: '16px' }}>
          <Button
            colorScheme="BlackAlpha.800"
            variant="link"
            style={{ marginRight: '7px' }}
            label="Προσωπικα Στοιχεια"
          />
        </Link>
      </Box>
    </Container>
  );
};

export default SettingsOptions;
