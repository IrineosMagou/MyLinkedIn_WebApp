// Layout.jsx
import React from 'react';
import Navbar from './myreuse/Navbar'; // Import the Navbar component

const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main>{children}</main>
    </div>
  );
};

export default Layout;
