import React, { useState } from 'react';
import './index.css'

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      onSearch(query);
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
        onKeyPress={handleKeyPress}
        className="search-input"
      />
    </div>
  );
}

export default SearchBar;
