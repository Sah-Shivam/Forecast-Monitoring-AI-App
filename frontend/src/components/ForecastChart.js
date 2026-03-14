import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { Box, Typography } from '@mui/material';

const ForecastChart = ({ data }) => {
  const chartData = data.actuals.map((actual, index) => ({
    time: format(new Date(actual.time), 'dd/MM HH:mm'),
    actual: actual.generation,
    forecast: data.forecasts[index]?.generation || null,
    fullTime: actual.time
  }));

  const calculateMetrics = () => {
    if (!data.actuals.length || !data.forecasts.length) return null;
    
    const errors = data.actuals.map((actual, i) => {
      if (data.forecasts[i]) {
        return Math.abs(actual.generation - data.forecasts[i].generation);
      }
      return null;
    }).filter(e => e !== null);
    
    if (errors.length === 0) return null;
    
    const mean = errors.reduce((a, b) => a + b, 0) / errors.length;
    const median = errors.sort((a, b) => a - b)[Math.floor(errors.length / 2)];
    const p95 = errors[Math.floor(errors.length * 0.95)];
    const p99 = errors[Math.floor(errors.length * 0.99)];
    
    return { mean, median, p95, p99 };
  };

  const metrics = calculateMetrics();

  return (
    <Box>
      {metrics && (
        <Box sx={{ mb: 2, p: 2, bgcolor: '#f8f9fa', borderRadius: 1 }}>
          <Typography variant="subtitle2" gutterBottom>Error Metrics (MW):</Typography>
          <Typography variant="body2">Mean: {metrics.mean.toFixed(2)}</Typography>
          <Typography variant="body2">Median: {metrics.median.toFixed(2)}</Typography>
          <Typography variant="body2">P95: {metrics.p95.toFixed(2)}</Typography>
          <Typography variant="body2">P99: {metrics.p99.toFixed(2)}</Typography>
        </Box>
      )}
      
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="time" 
            angle={-45}
            textAnchor="end"
            height={80}
            interval="preserveStartEnd"
          />
          <YAxis label={{ value: 'Generation (MW)', angle: -90, position: 'insideLeft' }} />
          <Tooltip 
            labelFormatter={(label) => `Time: ${label}`}
            formatter={(value) => [`${value.toFixed(2)} MW`, '']}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="actual" 
            stroke="#2196f3" 
            name="Actual Generation"
            dot={false}
            strokeWidth={2}
          />
          <Line 
            type="monotone" 
            dataKey="forecast" 
            stroke="#4caf50" 
            name="Forecast Generation"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default ForecastChart;