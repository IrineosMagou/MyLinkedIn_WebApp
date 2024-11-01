import React from 'react';
import {Button as MUIButton} from '@mui/material';

function Button({ onClick, label, disabled, type = 'button', className }) {
  return (
    <MUIButton
      onClick={onClick}
      disabled={disabled}
      type={type}
      className={`btn ${className}`}
    >
      {label}
    </MUIButton>
  );
}

export default Button;
