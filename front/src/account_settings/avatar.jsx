import React, { useState } from 'react';
import { Avatar, Popover, Button as MUIButton, Box} from '@mui/material';
import { Link } from 'react-router-dom';
import Logout from './logout';

const AvatarClk = ({pic_id}) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget); // Open the popover
  };

  const handleClose = () => {
    setAnchorEl(null); // Close the popover
  };

  const open = Boolean(anchorEl);
  const id = open ? 'avatar-popover' : undefined;

  return (
    <>
      <Avatar
        src={`http://127.0.0.1:8000/pictures/${pic_id}.jpg`}
        alt="User Avatar"
        sx={{ cursor: 'pointer' }}
        onClick={handleClick}
      />
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
      >
        <Box sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
          <Link to="/upload_article" style={{ textDecoration: 'none', marginBottom: '8px' }}>
            <MUIButton onClick={handleClose}> Άρθρα</MUIButton>
          </Link>
          <Link to="/upload_ad" style={{ textDecoration: 'none', marginBottom: '8px' }}>
            <MUIButton onClick={handleClose}>Αγγελίες</MUIButton>
          </Link>
          <Link to="/account_settings" style={{ textDecoration: 'none', marginBottom: '8px' }}>
            <MUIButton onClick={handleClose}>Ρυθμίσεις Λογαριασμού</MUIButton>
          </Link>
          <Logout />
        </Box>
      </Popover>
    </>
  );
};

export default AvatarClk;
