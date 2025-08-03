import React, { useState } from 'react';
import {
  List,
  ListItem,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Chip,
  Box,
  Tab,
  Tabs
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import moment from 'moment';

const AgentLogsPanel = ({ logs }) => {
  const [selectedAgent, setSelectedAgent] = useState('all');
  const [expanded, setExpanded] = useState(false);

  const agents = ['all', 'chartanalyst', 'riskmanager', 'marketsentinel', 'macroforecaster', 'tacticbot', 'platformpilot'];
  
  const filteredLogs = selectedAgent === 'all' 
    ? logs 
    : logs.filter(log => log.agent_name === selectedAgent);

  const handleChange = (event, newValue) => {
    setSelectedAgent(newValue);
  };

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const getAgentColor = (agentName) => {
    const colors = {
      chartanalyst: 'primary',
      riskmanager: 'secondary',
      marketsentinel: 'info',
      macroforecaster: 'warning',
      tacticbot: 'success',
      platformpilot: 'default'
    };
    return colors[agentName] || 'default';
  };

  if (!logs.length) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <Typography variant="body2" color="textSecondary">
          No agent logs available
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Tabs
        value={selectedAgent}
        onChange={handleChange}
        variant="scrollable"
        scrollButtons="auto"
        sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}
      >
        {agents.map(agent => (
          <Tab
            key={agent}
            label={agent === 'all' ? 'All' : agent}
            value={agent}
            sx={{ minWidth: 'auto', textTransform: 'capitalize' }}
          />
        ))}
      </Tabs>

      <List sx={{ padding: 0, maxHeight: '250px', overflow: 'auto' }}>
        {filteredLogs.map((log, index) => (
          <Accordion 
            key={log.id || index}
            expanded={expanded === `panel${index}`}
            onChange={handleAccordionChange(`panel${index}`)}
            sx={{ mb: 1 }}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box display="flex" alignItems="center" width="100%">
                <Chip
                  label={log.agent_name}
                  color={getAgentColor(log.agent_name)}
                  size="small"
                  sx={{ mr: 2 }}
                />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  {log.symbol} - {log.reasoning?.substring(0, 50)}...
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {moment(log.timestamp).format('HH:mm:ss')}
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Box>
                <Typography variant="body2" gutterBottom>
                  <strong>Reasoning:</strong> {log.reasoning}
                </Typography>
                <Typography variant="body2" gutterBottom>
                  <strong>Confidence:</strong> {(log.confidence * 100).toFixed(1)}%
                </Typography>
                {log.data && (
                  <Box mt={1}>
                    <Typography variant="caption" display="block" gutterBottom>
                      <strong>Data:</strong>
                    </Typography>
                    <pre style={{ fontSize: '11px', overflow: 'auto', maxHeight: '100px' }}>
                      {JSON.stringify(log.data, null, 2)}
                    </pre>
                  </Box>
                )}
              </Box>
            </AccordionDetails>
          </Accordion>
        ))}
      </List>
    </Box>
  );
};

export default AgentLogsPanel;