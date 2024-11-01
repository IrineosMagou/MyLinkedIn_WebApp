import React, { useState } from 'react';
import Button from './myButton';

export function DropText({textAreaContent , setTextAreaContent , onClick}) {
  // State to track whether the textarea is visible
  const [isTextAreaVisible, setIsTextAreaVisible] = useState(false);
  // Function to toggle the textarea visibility
  const handleButtonClick = () => {
    setIsTextAreaVisible(!isTextAreaVisible);
  };
  const handleTextAreaChange = (event) => {
    setTextAreaContent(event.target.value);
  };

  return (
    <div>
      {/* Button to toggle textarea */}
      <Button label="Σχόλιο" onClick={handleButtonClick}>
        {isTextAreaVisible ? 'Hide' : 'Add Comment'}
      </Button>

      {/* Show textarea when isTextAreaVisible is true */}
      {isTextAreaVisible && (
        <div>
          <textarea placeholder="Write your comment here..." rows={4} cols={50} value={textAreaContent} onChange={handleTextAreaChange}></textarea>
          <Button label="Σχολιασε" onClick={onClick}/>
        </div>
      )}
    </div>
  );
}
