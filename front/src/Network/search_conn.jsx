import React, { useState } from "react";
import { TextField, Box } from '@mui/material';
import Button from "../myreuse/myButton"; // Assuming you are using a custom button component

function SearchBar({ onSearch }) {
  const [searchText, setSearchText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ target: { value: searchText } });
    setSearchText('');
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', alignItems: 'center', gap: 2 }}
    >
      <TextField
        id="search"
        type="text"
        value={searchText}
        placeholder="Search Profession..."
        variant="outlined"
        onChange={(e) => setSearchText(e.target.value)}
        sx={{ minWidth: '350px' }} // This will make the search bar bigger
      />
      <Button label="Search" type="submit" />
    </Box>
  );
}

export default SearchBar;
