import React from 'react';
import { useDropzone } from 'react-dropzone';

const FileDropzone = ({ onDrop }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif'],
      'video/*': ['.mp4', '.mkv', '.avi']
    }
  });

  return (
    <div
      {...getRootProps()}
      style={dropzoneStyles}
      role="button"
      tabIndex={0}
      aria-describedby="dropzone-description"
    >
      <input 
        {...getInputProps()} 
        aria-label="Upload your files by dragging or clicking here"
      />
      {isDragActive ? (
        <p id="dropzone-description">Drop the files here ...</p>
      ) : (
        <p id="dropzone-description">Drag 'n' drop some files here, or click to select files</p>
      )}
    </div>
  );
};

// Basic styling for the dropzone
const dropzoneStyles = {
  border: '2px dashed #cccccc',
  borderRadius: '4px',
  padding: '20px',
  textAlign: 'center',
  cursor: 'pointer'
};

export default FileDropzone;
