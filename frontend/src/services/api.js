import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const fetchForecastData = async (startDate, endDate, horizon) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/data`, {
      params: {
        start: startDate,
        end: endDate,
        horizon: horizon
      }
    });
    
    if (response.data.success) {
      return {
        actuals: response.data.actuals,
        forecasts: response.data.forecasts
      };
    } else {
      throw new Error(response.data.error || 'Failed to fetch data');
    }
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const fetchStats = async (startDate, endDate) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stats`, {
      params: {
        start: startDate,
        end: endDate
      }
    });
    
    if (response.data.success) {
      return response.data.errors_by_horizon;
    } else {
      throw new Error(response.data.error || 'Failed to fetch stats');
    }
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};