import React, { useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

function WeatherSummary({weather}) {
  if (!weather) return null;

  const jsonData = JSON.parse(weather.generation);
  const summary = jsonData.output;

  return (
    <article>
      <h2><b>{weather.temperature}&deg;C</b></h2>
      <h3><b>{weather.description}</b></h3>
      {/* other summary data */}
      <p>{summary.split('\n\n').map(p => <p key={p}>{p}</p>)}</p> 
    </article>
  );
}

WeatherSummary.propTypes = {
  weather: PropTypes.object
};

function Weather() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function fetchWeather() {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`/weather/${city}`);
      setWeather(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h1>Weather App</h1>

      <input 
        value={city}
        onChange={e => setCity(e.target.value)}
      />

      <button onClick={fetchWeather}>Get Weather</button>

      {loading && <p>Loading...</p>}

      {error && <p>Error fetching weather data</p>}

      {weather && (
        <article>
          <h2>{city}</h2>
          <WeatherSummary weather={weather} />
        </article>
      )}
    </section>
  );
}

export default Weather;