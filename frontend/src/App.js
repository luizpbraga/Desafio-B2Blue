import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Grid, Paper, ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';
import StationCard from './components/StationCard';
import HistoryTable from './components/HistoryTable';
import { api, endpoints } from './services/api';

function App() {
  const [stations, setStations] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar os dados iniciais
  useEffect(() => {
    fetchData();
  }, []);

  // Função para buscar todas as estações e histórico
  const fetchData = async () => {
    setLoading(true);
    try {
      const [stationsRes, historyRes] = await Promise.all([
        api.get(endpoints.stations),
        api.get(endpoints.history)
      ]);
      
      setStations(stationsRes.data);
      setHistory(historyRes.data);
      setError(null);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setError('Falha ao carregar os dados. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Atualizar o volume de uma estação
  const updateStationVolume = async (stationId, newPercentage) => {
    try {
      const response = await api.patch(`${endpoints.stations}${stationId}/`, {
        volume_percentage: newPercentage
      });
      
      // Atualizar a lista de estações
      setStations(stations.map(s => 
        s.id === stationId ? response.data : s
      ));
      
      // Recarregar o histórico
      const historyRes = await api.get(endpoints.history);
      setHistory(historyRes.data);
      
    } catch (err) {
      console.error('Erro ao atualizar volume:', err);
      alert('Falha ao atualizar o volume. Por favor, tente novamente.');
    }
  };

  // Confirmar coleta de resíduos
  const confirmCollection = async (stationId) => {
    try {
      const response = await api.post(`${endpoints.stations}${stationId}/confirm_collection/`);
      
      // Atualizar a lista de estações
      setStations(stations.map(s => 
        s.id === stationId ? response.data.station : s
      ));
      
      // Recarregar o histórico
      const historyRes = await api.get(endpoints.history);
      setHistory(historyRes.data);
      
    } catch (err) {
      console.error('Erro ao confirmar coleta:', err);
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
          
          {error && (
            <Paper 
              elevation={3} 
              sx={{ p: 2, mb: 3, bgcolor: 'error.light', color: 'error.contrastText' }}
            >
              <Typography>{error}</Typography>
            </Paper>
          )}
          
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
