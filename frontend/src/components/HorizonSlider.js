import React from 'react';
import { Box, Slider, Typography } from '@mui/material';

const HorizonSlider = ({ horizon, onHorizonChange }) => {
  const handleChange = (event, newValue) => {
    onHorizonChange(newValue);
  };

  return (
    <Box>
      <Typography variant="subtitle2" gutterBottom>
        Minimum Forecast Horizon: {horizon} hours
      </Typography>
      <Slider
        value={horizon}
        onChange={handleChange}
        min={0}
        max={48}
        step={1}
        marks={[
          { value: 0, label: '0h' },
          { value: 12, label: '12h' },
          { value: 24, label: '24h' },
          { value: 36, label: '36h' },
          { value: 48, label: '48h' }
        ]}
        valueLabelDisplay="auto"
      />
    </Box>
  );
};

export default HorizonSlider;