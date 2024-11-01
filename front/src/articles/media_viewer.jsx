
const MediaViewer = ({ fileUrls , art_id}) => {
  return (
    <div>
      {fileUrls.map((fileUrl, index) => {
        const fileExtension = fileUrl.split('.').pop().toLowerCase();
        // Determine how to render based on file type
        if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
          // Render image files
          return (
            <div key={index}>
              <img src={'http://127.0.0.1:8000/media/article' + art_id + '/' + fileUrl} alt={`media-${index}`} style={{ maxWidth: '100%', height: 'auto' }} />
            </div>
          );
        } else if (['mp4', 'webm', 'ogg'].includes(fileExtension)) {
          // Render video files
          return (
            <div key={index}>
              <video controls style={{ maxWidth: '100%', height: 'auto' }}>
                <source src={'http://127.0.0.1:8000' + fileUrl} type={`video/${fileExtension}`} />
                Your browser does not support the video tag.
              </video>
            </div>
          );
        } else {
          // Handle other file types
          return <div key={index}>Unsupported file type: {fileExtension}</div>;
        }
      })}
    </div>
  );
};
export default MediaViewer
