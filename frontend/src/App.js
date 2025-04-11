import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Grid, Paper, ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';
import StationCard from './components/StationCard';
import HistoryTable from './components/HistoryTable';
import { api, endpoints } from './services/api';

/**
 * Main application component for the Storage Control System.
 * Manages station data, operation history, and provides UI for user interactions.
 */
function App() {
  const [stations, setStations] = useState([]); // Array of station objects
  const [history, setHistory] = useState([]);    // Array of historical operations
  const [loading, setLoading] = useState(true); // Loading state flag
  const [error, setError] = useState(null);     // Error message state

  /**
   * Effect hook to load initial data when component mounts.
   * Fetches both stations and history data simultaneously.
   */
  useEffect(() => {
    fetchData();
  }, []);

  /**
   * Fetches all stations and history data from the API.
   * Handles loading states and errors during the fetch operation.
   */
  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch both stations and history data in parallel
      const [stationsRes, historyRes] = await Promise.all([
        api.get(endpoints.stations),
        api.get(endpoints.history)
      ]);
      
      setStations(stationsRes.data);
      setHistory(historyRes.data);
      setError(null);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Falha ao carregar os dados. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Updates the volume percentage for a specific station.
   * @param {string} stationId - ID of the station to update
   * @param {number} newPercentage - New volume percentage value (0-100)
   */
  const updateStationVolume = async (stationId, newPercentage) => {
    try {
      const response = await api.patch(`${endpoints.stations}${stationId}/`, {
        volume_percentage: newPercentage
      });
      
      // Update the station in the local state
      setStations(stations.map(s => 
        s.id === stationId ? response.data : s
      ));
      
      // Refresh history data
      const historyRes = await api.get(endpoints.history);
      setHistory(historyRes.data);
      
    } catch (err) {
      console.error('Error updating volume:', err);
      alert('Falha ao atualizar o volume. Por favor, tente novamente.');
    }
  };

  /**
   * Confirms waste collection for a specific station.
   * Resets the station's volume and records the collection event.
   * @param {string} stationId - ID of the station to confirm collection
   */
  const confirmCollection = async (stationId) => {
    try {
      const response = await api.post(`${endpoints.stations}${stationId}/confirm_collection/`);
      
      // Update the station in the local state
      setStations(stations.map(s => 
        s.id === stationId ? response.data.station : s
      ));
      
      // Refresh history data
      const historyRes = await api.get(endpoints.history);
      setHistory(historyRes.data);
      
    } catch (err) {
      console.error('Error confirming collection:', err);
      alert('Falha ao confirmar a coleta. Por favor, tente novamente.');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center" color="primary">
            Sistema de Controle de Armazenamento - B2Blue
          </Typography>
          
          {/* Error display */}
          {error && (
            <Paper 
              elevation={3} 
              sx={{ p: 2, mb: 3, bgcolor: 'error.light', color: 'error.contrastText' }}
            >
              <Typography>{error}</Typography>
            </Paper>
          )}
          
          {/* Stations grid */}
          <Grid container spacing={4} sx={{ mb: 4 }}>
            {stations.map((station) => (
              <Grid item xs={12} md={4} key={station.id}>
                <StationCard 
                  station={station}
                  onUpdateVolume={updateStationVolume}
                  onConfirmCollection={confirmCollection}
                />
              </Grid>
            ))}
          </Grid>
          
          {/* History section */}
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom color="primary">
              Histórico de Operações
            </Typography>
            <HistoryTable history={history} loading={loading} />
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
