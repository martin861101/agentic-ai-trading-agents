import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Typography,
  Box,
  Tab,
  Tabs,
  Tooltip
} from '@mui/material';
import moment from 'moment';

const TradeBook = ({ trades, decisions }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const getSignalColor = (signal) => {
    switch (signal) {
      case 'BUY': return 'success';
      case 'SELL': return 'error';
      case 'HOLD': return 'warning';
      default: return 'default';
    }
  };

  const getPnLColor = (pnl) => {
    if (pnl > 0) return 'success';
    if (pnl < 0) return 'error';
    return 'default';
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const DecisionsTable = () => (
    <TableContainer component={Paper} sx={{ maxHeight: 300 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell>Time</TableCell>
            <TableCell>Symbol</TableCell>
            <TableCell>Signal</TableCell>
            <TableCell>Confidence</TableCell>
            <TableCell>Agents</TableCell>
            <TableCell>Reasoning</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {decisions.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} align="center">
                <Typography variant="body2" color="textSecondary">
                  No trading decisions yet
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            decisions.map((decision, index) => (
              <TableRow key={index}>
                <TableCell>
                  <Typography variant="caption">
                    {moment(decision.timestamp).format('HH:mm:ss')}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontWeight="bold">
                    {decision.symbol}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={decision.signal}
                    color={getSignalColor(decision.signal)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {(decision.confidence * 100).toFixed(1)}%
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="caption">
                    {decision.contributing_agents?.length || 0} agents
                  </Typography>
                </TableCell>
                <TableCell>
                  <Tooltip title={decision.reasoning}>
                    <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                      {decision.reasoning}
                    </Typography>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );

  const TradesTable = () => (
    <TableContainer component={Paper} sx={{ maxHeight: 300 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell>Entry Time</TableCell>
            <TableCell>Exit Time</TableCell>
            <TableCell>Symbol</TableCell>
            <TableCell>Entry Price</TableCell>
            <TableCell>Exit Price</TableCell>
            <TableCell>P&L</TableCell>
            <TableCell>P&L %</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {trades.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} align="center">
                <Typography variant="body2" color="textSecondary">
                  No completed trades yet
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            trades.map((trade, index) => (
              <TableRow key={index}>
                <TableCell>
                  <Typography variant="caption">
                    {moment(trade.entry_time).format('MM/DD HH:mm')}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="caption">
                    {trade.exit_time ? moment(trade.exit_time).format('MM/DD HH:mm') : '-'}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" fontWeight="bold">
                    {trade.symbol}
                  </Typography>
                </TableCell>
                <TableCell>
                  {formatCurrency(trade.entry_price)}
                </TableCell>
                <TableCell>
                  {trade.exit_price ? formatCurrency(trade.exit_price) : '-'}
                </TableCell>
                <TableCell>
                  <Typography color={getPnLColor(trade.pnl)}>
                    {trade.pnl ? formatCurrency(trade.pnl) : '-'}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography color={getPnLColor(trade.pnl_percentage)}>
                    {trade.pnl_percentage ? `${trade.pnl_percentage.toFixed(2)}%` : '-'}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={trade.success_flag ? 'Profit' : 'Loss'}
                    color={trade.success_flag ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );

  return (
    <Box>
      <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 2 }}>
        <Tab label={`Decisions (${decisions.length})`} />
        <Tab label={`Completed Trades (${trades.length})`} />
      </Tabs>
      
      {activeTab === 0 && <DecisionsTable />}
      {activeTab === 1 && <TradesTable />}
    </Box>
  );
};

export default TradeBook;