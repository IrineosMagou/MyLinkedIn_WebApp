import React, { useEffect, useState } from 'react';
import SearchBar from './search_conn';
import debounce from '../myreuse/debounce';
import UserGrid from './user_profile';
import ConnectedUsers from './net_grid';

const Network = () => {
  const accessToken = localStorage.getItem('accessToken');
  const [error, setError] = useState(null);
  const [users, setUsers] = useState([]);
  
  
//==================================FOR_CONNECTIONS============================
useEffect(() => {
    const fetchConnections = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/user_conn' , {
          headers: {'Authorization': `Bearer ${accessToken}`}
        }); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setUsers(data.data);
        console.log(data.data);

      } catch (error) {
        setError(error.message);
      }
    };
    fetchConnections();
  }, []);
//==================================FOR_SEARCH=================================
// ============================================================================
  const handleSearch = async (e) => {
      const searchQuery = e.target.value;
      debouncedSearch(searchQuery);
  }
  const debouncedSearch = debounce(async (searchQuery) => {
      try {
      const response = await fetch('http://127.0.0.1:8000/user_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ query: searchQuery }),
      });
      if (response.status === 404) {
        setError('Δεν υπάρχουν Χρήστες με αυτό το επάγγελμα')
      }
      else if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      else{
        const data = await response.json();
        setError(null);
        setUsers(data.data); // Assuming your state variable for search results is 'users'
        console.log(data.data);

      }
    } catch (error) {
      setError(error.message);
    } 
  }, 300);

  return(
    <>
      <SearchBar
        onSearch={handleSearch}
      />
      {error ? (
        <p>{error}</p>
      ) : (
        !users ? (
          <>
        <ConnectedUsers />
        </>
      ):(
            <UserGrid users = {users} />       
      )
    )}
    </>
  )
}

export default Network