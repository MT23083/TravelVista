import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import Card from './components/Card';
import HotelList from './components/HotelList';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);
  const [showHotelList, setShowHotelList] = useState(false); // New state variable

  // Function to handle search
  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/process_text', {
        params: { text: query },
      });
      const sortedResults = response.data.results.sort((a, b) => b.metadata.Rating - a.metadata.Rating);
      setResults(sortedResults);
      setShowHotelList(false); // Reset to show Card component
    } catch (error) {
      setError('An error occurred while fetching results');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle city selection
  const handleCityClick = (cityName) => {
    setSelectedCity(cityName);
    setShowHotelList(true); // Show HotelList component
  };

  // Render Card or HotelList based on showHotelList state
  return (
    <div className="App">
      <SearchBar onSearch={handleSearch} />
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {!showHotelList ? ( // Render Card component
        results.length > 0 ? (
          <div className="card-container">
            {results.map((result) => (
              <Card key={result.id} result={result} onClick={() => handleCityClick(result.metadata.Response)} onCityClick={handleCityClick} />
            ))}
          </div>
        ) : (
          <p>No results available.</p>
        )
      ) : (
        // Render HotelList component
        <HotelList city={selectedCity} />
      )}
    </div>
  );
}

export default App;
