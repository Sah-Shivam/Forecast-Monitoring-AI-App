import React, { useState, useEffect } from 'react';
import { Container, AppBar, Toolbar, Typography, Box, Paper } from '@mui/material';
import TimeRangePicker from './components/TimeRangePicker';
import HorizonSlider from './components/HorizonSlider';
import ForecastChart from './components/ForecastChart';
import { fetchForecastData } from './services/api';

function App() {
  const [startDate, setStartDate] = useState(new Date('2024-01-01'));
  const [endDate, setEndDate] = useState(new Date('2024-01-07'));
  const [horizon, setHorizon] = useState(4);
  const [data, setData] = useState({ actuals: [], forecasts: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [startDate, endDate, horizon]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchForecastData(
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0],
        horizon
      );
      setData(result);
    } catch (err) {
      setError('Failed to fetch data. Please try again.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit'
    }).replace(/\//g, '/');
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: '#f5f5f5' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            UK Wind Power Forecast Monitor
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            <Box sx={{ flex: 1 }}>
              <TimeRangePicker
                startDate={startDate}
                endDate={endDate}
                onStartDateChange={setStartDate}
                onEndDateChange={setEndDate}
              />
            </Box>
            <Box sx={{ flex: 1 }}>
              <HorizonSlider
                horizon={horizon}
                onHorizonChange={setHorizon}
              />
            </Box>
          </Box>
        </Paper>

        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="subtitle1" color="text.secondary" gutterBottom>
            Showing forecasts created at least {horizon} hours before target time
          </Typography>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Time Range: {formatDate(startDate)} - {formatDate(endDate)}
          </Typography>
          
          {loading && <Typography>Loading data...</Typography>}
          {error && <Typography color="error">{error}</Typography>}
          
          {!loading && !error && data.actuals.length === 0 && (
            <Typography>No data available for selected range</Typography>
          )}
          
          {!loading && !error && data.actuals.length > 0 && (
            <ForecastChart data={data} />
          )}
        </Paper>
      </Container>
    </Box>
  );
}

export default App;