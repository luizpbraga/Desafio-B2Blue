import React from 'react';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper, 
  Chip,
  CircularProgress,
  Box,
  Typography
} from '@mui/material';

/**
 * Determines the display properties for different operation types.
 * @param {string} type - The operation type (create, update, collection_request, collection_complete)
 * @returns {object} An object containing color and label for the operation chip
 */
const getOperationInfo = (type) => {
  switch (type) {
    case 'create':
      return { color: 'info', label: 'Criação' };
    case 'update':
      return { color: 'primary', label: 'Atualização' };
    case 'collection_request':
      return { color: 'warning', label: 'Solicitação de Coleta' };
    case 'collection_complete':
      return { color: 'success', label: 'Coleta Concluída' };
    default:
      return { color: 'default', label: type };
  }
};

/**
 * Displays a table of historical operations for waste collection stations.
 * Shows loading state and empty state when appropriate.
 * @param {object} props - Component props
 * @param {Array} props.history - Array of history records
 * @param {boolean} props.loading - Loading state flag
 */
const HistoryTable = ({ history, loading }) => {
  // Loading state
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  // Empty state
  if (history.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Nenhum registro histórico encontrado.
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} elevation={0}>
      <Table sx={{ minWidth: 650 }} aria-label="tabela de histórico">
        <TableHead>
          <TableRow>
            <TableCell>Estação</TableCell>
            <TableCell>Operação</TableCell>
            <TableCell align="right">Volume (%)</TableCell>
            <TableCell>Data/Hora</TableCell>
            <TableCell>Observações</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {history.map((record) => {
            const operationInfo = getOperationInfo(record.operation_type);
            
            return (
              <TableRow
                key={record.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {record.station_name}
                </TableCell>
                <TableCell>
                  <Chip 
                    label={operationInfo.label}
                    color={operationInfo.color}
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">{record.volume_percentage}%</TableCell>
                <TableCell>
                  {new Date(record.timestamp).toLocaleString()}
                </TableCell>
                <TableCell>{record.notes}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default HistoryTable;
