import React, { useState } from 'react';
import './index.css';

function Card({ result, onClick, onCityClick }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleExpandClick = () => {
    setIsExpanded(!isExpanded);
  };

  const getRatingColor = (rating) => {
    if (rating >= 4) {
      return '#efffe0'; 
    } else if (rating >= 3 && rating < 4) {
      return '#fef9e7'; 
    } else {
      return '#fce7e6';
    }
  };

  const handleTitleClick = () => {
    // Call the onCityClick function passed from the parent component with the city name
    onCityClick(result.metadata.Response);
  };

  return (
    <div className="card">
      <div className="card-header">
        {/* Make the title clickable */}
        <h3>
          <a href="#" onClick={handleTitleClick}>
            {result.metadata.Response}
          </a>
        </h3>
        <div className="rating-box" style={{ backgroundColor: getRatingColor(result.metadata.Rating.toFixed(1)) }}>
          <p>Rating: {result.metadata.Rating.toFixed(2)}</p>
        </div>
      </div>
      <div className="content-container">
        <p className="card-content">{isExpanded ? result.page_content : result.page_content.substring(0, 100) + "..."}</p>
        <div className="rating-and-expand">
          <span className="expand-text" onClick={handleExpandClick}>
            {isExpanded ? 'View Less' : 'View More'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Card;
