import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HotelList.css'; 

function HotelList({ city }) {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
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

  useEffect(() => {
    const fetchHotelData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await axios.post('http://192.168.66.22:9002/hotel_rank', {
          city: city
        });

        setHotels(response.data.places_with_reviews);
      } catch (error) {
        setError('An error occurred while fetching hotel data');
      } finally {
        setLoading(false);
      }
    };

    fetchHotelData();
  }, [city]);

  return (
    <div className="hotel-list">
      <h2>Hotels in {city}</h2>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {hotels.length > 0 && (
        <ul>
          {hotels.map((hotel, index) => (
            <li key={index} className="hotel-item">
              <div className="hotel-info">
                <h3>{hotel.name}</h3>
                <div className="rating-box" style={{ backgroundColor: getRatingColor(hotel.overall_score.toFixed(1)) }}>
                  <p>Rating: {hotel.overall_score.toFixed(1)}</p>
                </div>
              </div>
              <div className="address-review">
                <p>{hotel.address[0]}</p>
                <p className="review">Review: {hotel.reviews[0].text}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
      {hotels.length === 0 && !loading && <p>No hotels found in {city}</p>}
    </div>
  );
}

export default HotelList;
