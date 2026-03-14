import React from 'react';
import { Box, TextField, Typography } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const TimeRangePicker = ({ startDate, endDate, onStartDateChange, onEndDateChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <Typography variant="subtitle2" gutterBottom>Select Time Range</Typography>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <DatePicker
            label="Start Date"
            value={startDate}
            onChange={onStartDateChange}
            renderInput={(params) => <TextField {...params} size="small" />}
          />
          <DatePicker
            label="End Date"
            value={endDate}
            onChange={onEndDateChange}
            renderInput={(params) => <TextField {...params} size="small" />}
          />
        </Box>
      </Box>
    </LocalizationProvider>
  );
};

export default TimeRangePicker;