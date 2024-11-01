import React from 'react';
import RouterSetup from './';
import { AuthProvider } from './contextProvider';

function App() {
  return (
    <div>    
        <AuthProvider>
          <RouterSetup />
        </AuthProvider>
      
    </div>
  );
}

export default App;