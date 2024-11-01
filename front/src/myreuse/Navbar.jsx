import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button as MUIButton, Box } from '@mui/material';
import AvatarClk from '../account_settings/avatar';
import { useAuth } from '../contextProvider';

const Navbar = () => {
    const { accessToken, idPic } = useAuth();
    const [token, setToken] = useState(accessToken);

    useEffect(() => {
        setToken(accessToken);
    }, [accessToken]);

    return (
        <AppBar position="static" sx={{ backgroundColor: 'purple', padding: 2 }}>
            <Toolbar sx={{ justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {!token ? (
                        <>
                            <Link to='/SignIn' style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Συνδεση
                                </MUIButton>
                            </Link>
                            <Link to="/SignUp" style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Εγγραφη
                                </MUIButton>
                            </Link>
                        </>
                    ) : (
                        <>
                            <AvatarClk pic_id={idPic} />
                            <Link to="/network" style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Δικτυο
                                </MUIButton>
                            </Link>
                            <Link to="/user_notifications" style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Ειδοποιησεις
                                </MUIButton>
                            </Link>
                            
                        </>
                    )}
                </Box>
                
                <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center' }}>
                    {token ? (
                        <Link to="/" style={{ textDecoration: 'none' }}>
                            <Typography variant="h6" sx={{ color: 'white', cursor: 'pointer' }}>
                                OzzyLink
                            </Typography>
                        </Link>
                    ) : (
                        <Typography variant="h6" sx={{ color: 'white' }}>
                            OzzyLink
                        </Typography>
                    )}
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {token && (
                        <>
                            <Link to="/ads" style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Αγγελιες
                                </MUIButton>
                            </Link>
                            <Link to="/chat" style={{ textDecoration: 'none' }}>
                                <MUIButton variant="contained" color="inherit">
                                    Συζητησεις
                                </MUIButton>
                            </Link>
                        </>
                    )}
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;
