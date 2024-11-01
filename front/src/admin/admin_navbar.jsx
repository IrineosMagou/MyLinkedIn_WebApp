import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button as MUIButton } from '@mui/material';
import Logout from '../account_settings/logout';

const AdNavbar = () => {
    return (
        <AppBar position="static" sx={{ backgroundColor: 'purple' }}>
            <Toolbar>
                <Link to="/admin_users" style={{ textDecoration: 'none' }}>
                    <MUIButton variant="contained" color="inherit">
                        Χρήστες
                    </MUIButton>
                </Link>
                <Logout />
                <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', color: 'white' }}>
                    OzzyLink
                </Typography>
            </Toolbar>
        </AppBar>
    );
};

export default AdNavbar;
