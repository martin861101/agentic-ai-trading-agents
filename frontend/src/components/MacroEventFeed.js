import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Typography,
  Chip,
  Box
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Announcement,
  AttachMoney,
  Public
} from '@mui/icons-material';
import moment from 'moment';

const MacroEventFeed = ({ events }) => {
  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'NEWS': return <Announcement />;
      case 'ECONOMIC': return <AttachMoney />;
      case 'EARNINGS': return <TrendingUp />;
      default: return <Public />;
    }
  };

  const getBiasIcon = (bias) => {
    switch (bias) {
      case 'BULLISH': return <TrendingUp color="success" />;
      case 'BEARISH': return <TrendingDown color="error" />;
      case 'NEUTRAL': return <TrendingFlat color="action" />;
      default: return <TrendingFlat />;
    }
  };

  const getBiasColor = (bias) => {
    switch (bias) {
      case 'BULLISH': return 'success';
      case 'BEARISH': return 'error';
      case 'NEUTRAL': return 'default';
      default: return 'default';
    }
  };

  if (!events.length) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <Typography variant="body2" color="textSecondary">
          No macro events available
        </Typography>
      </Box>
    );
  }

  return (
    <List sx={{ padding: 0 }}>
      {events.map((event, index) => (
        <ListItem key={index} divider sx={{ py: 1 }}>
          <ListItemIcon>
            {getEventIcon(event.event_type)}
          </ListItemIcon>
          <ListItemText
            primary={
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="subtitle2">
                  {event.event_name}
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  {getBiasIcon(event.forecast_bias)}
                  <Chip
                    label={event.forecast_bias}
                    color={getBiasColor(event.forecast_bias)}
                    size="small"
                  />
                </Box>
              </Box>
            }
            secondary={
              <Box>
                <Typography variant="body2" color="textSecondary">
                  Impact Score: {event.impact_score}/10 • Source: {event.source}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {moment(event.event_time).format('MMM DD, HH:mm')}
                </Typography>
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default MacroEventFeed;