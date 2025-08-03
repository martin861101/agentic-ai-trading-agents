import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Chip,
  Alert
} from '@mui/material';
import LiveSignalFeed from './components/LiveSignalFeed';
import ChartOverlay from './components/ChartOverlay';
import AgentLogsPanel from './components/AgentLogsPanel';
import MacroEventFeed from './components/MacroEventFeed';
import TradeBook from './components/TradeBook';
import { SignalWebSocket } from './services/websocket';
import './App.css';

function App() {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [signals, setSignals] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [agentLogs, setAgentLogs] = useState([]);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new SignalWebSocket('ws://localhost:8007/ws');
    
    ws.onMessage((data) => {
      handleWebSocketMessage(data);
    });

    ws.ws.onopen = () => setConnectionStatus('connected');
    ws.ws.onclose = () => setConnectionStatus('disconnected');
    ws.ws.onerror = () => setConnectionStatus('error');

    // Add sample data for demo
    setTimeout(() => {
      setSignals([
        {
          agent_name: 'chartanalyst',
          symbol: 'EURUSD',
          signal_type: 'BUY',
          confidence: 0.85,
          reasoning: 'Bullish engulfing pattern detected',
          timestamp: new Date().toISOString()
        }
      ]);
      
      setAgentLogs([
        {
          id: 1,
          agent_name: 'chartanalyst',
          symbol: 'EURUSD',
          confidence: 0.85,
          reasoning: 'Strong bullish pattern with volume confirmation',
          timestamp: new Date().toISOString(),
          data: { pattern: 'bullish_engulfing', strength: 8.5 }
        }
      ]);
    }, 2000);

    return () => {
      ws.ws.close();
    };
  }, []);

  const handleWebSocketMessage = (data) => {
    console.log('WebSocket message:', data);
  };

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'success';
      case 'disconnected': return 'error';
      case 'error': return 'error';
      default: return 'warning';
    }
  };

  return (
    <div className="App">
      <AppBar position="static" sx={{ backgroundColor: '#1a1a1a' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🤖 Agentic AI Trading System
          </Typography>
          <Chip 
            label={`Connection: ${connectionStatus}`}
            color={getStatusColor()}
            variant="outlined"
          />
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 2 }}>
        <Grid container spacing={2}>
          {/* Top Row - Charts and Live Feed */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                📈 Chart Analysis
              </Typography>
              <ChartOverlay decisions={decisions} />
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, height: '400px', overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>
                📡 Live Signals
              </Typography>
              <LiveSignalFeed signals={signals} />
            </Paper>
          </Grid>

          {/* Middle Row - Agent Logs and Macro Events */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: '350px', overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>
                🧠 Agent Intelligence
              </Typography>
              <AgentLogsPanel logs={agentLogs} />
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: '350px', overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>
                🌍 Macro Events
              </Typography>
              <MacroEventFeed events={[]} />
            </Paper>
          </Grid>

          {/* Bottom Row - Trade Book */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                📊 Trade Book
              </Typography>
              <TradeBook trades={[]} decisions={decisions} />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default App;
