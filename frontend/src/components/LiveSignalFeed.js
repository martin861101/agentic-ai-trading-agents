import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  Chip,
  Box,
  Typography,
  Avatar
} from '@mui/material';
import moment from 'moment';

const LiveSignalFeed = ({ signals }) => {
  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'BUY': return 'success';
      case 'SELL': return 'error';
      case 'HOLD': return 'warning';
      default: return 'default';
    }
  };

  const getAgentAvatar = (agentName) => {
    const avatars = {
      chartanalyst: '📈',
      riskmanager: '🛡️',
      marketsentinel: '👁️',
      macroforecaster: '🌍',
      tacticbot: '🎯',
      platformpilot: '🤖'
    };
    return avatars[agentName] || '🔍';
  };

  if (!signals.length) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <Typography variant="body2" color="textSecondary">
          Waiting for signals...
        </Typography>
      </Box>
    );
  }

  return (
    <List sx={{ padding: 0 }}>
      {signals.map((signal, index) => (
        <ListItem key={index} divider sx={{ py: 1 }}>
          <Avatar sx={{ mr: 2, bgcolor: 'transparent', fontSize: '1.2em' }}>
            {getAgentAvatar(signal.agent_name)}
          </Avatar>
          <ListItemText
            primary={
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="subtitle2">
                  {signal.symbol}
                </Typography>
                <Chip
                  label={signal.signal_type || 'ANALYSIS'}
                  color={getSignalColor(signal.signal_type)}
                  size="small"
                />
              </Box>
            }
            secondary={
              <Box>
                <Typography variant="body2" color="textSecondary">
                  {signal.agent_name}: {signal.reasoning}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Confidence: {(signal.confidence * 100).toFixed(1)}% • 
                  {moment(signal.timestamp).fromNow()}
                </Typography>
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default LiveSignalFeed;