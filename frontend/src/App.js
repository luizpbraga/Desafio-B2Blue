import React from 'react';
import { Container, Typography, Box, ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center" color="primary">
            Sistema de Controle de Armazenamento - B2Blue
          </Typography>
          {/* Componentes serão adicionados aqui */}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
