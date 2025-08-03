import React from 'react';
import { Box, Typography } from '@mui/material';

const ChartOverlay = ({ decisions }) => {
  return (
    <Box sx={{ height: '100%', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Typography variant="h6" color="textSecondary">
        📊 Trading Chart (TradingView integration placeholder)
      </Typography>
    </Box>
  );
};

export default ChartOverlay;