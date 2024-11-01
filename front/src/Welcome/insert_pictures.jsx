import React from 'react';

const ProfilePicture = ({setSelectedFile}) => {

  const handleFileChange = (e) => {
    e.preventDefault();
    const newFile = e.target.files[0];
    setSelectedFile(newFile);

  };

  // const handleUpload = async (e) => {
  //   e.preventDefault();
  //   const formData = new FormData();

  //   if (selectedFile.length === 0) {
  //     alert('Please select a picture to upload.');
  //     return;
  //   }
  //   else {
  //     formData.append('picture', selectedFile);
  //     for (const pair of formData.entries()) {
  //       console.log(pair[0] + ': ' + pair[1]);
  //     }
  //  }


  //   const accessToken = localStorage.getItem("accessToken");
  //   console.log(accessToken)
  //   try{
  //   const response =  await fetch('http://127.0.0.1:8000/user_profile/picture', {
  //     method: 'POST',
  //     headers: {'Authorization': `Bearer ${accessToken}`},
  //     body: formData,
  //   })
  //     if (response.ok) {
  //     // Request was successful
  //       console.log('Success:', response);
  //       history("/")

  //   } else {
  //     // Handle errors
  //       console.error('Error:', response);
  //   }
  // } catch (error) {
  //   // Handle network or other errors
  //     console.error('Error:', error);
  // }
  // };

  return (
    <div>
      <h3>Ανέβασε Φωτογραφία</h3>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      {/* <button onClick={handleUpload}>Upload</button> */}
    </div>
  );
};

export default ProfilePicture;
