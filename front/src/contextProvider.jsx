// contextProvider.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
    const [idPic , setIdPic]= useState(localStorage.getItem('id'));
   
    console.log(idPic);

    return (
        <AuthContext.Provider value={{ accessToken, setAccessToken , idPic , setIdPic }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
