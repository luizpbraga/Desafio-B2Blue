import React, { useState } from 'react';
import { 
  Card, 
  CardHeader, 
  CardContent, 
  CardActions, 
  Button, 
  Typography, 
  Slider, 
  Box, 
  LinearProgress, 
  Chip 
} from '@mui/material';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import WarningIcon from '@mui/icons-material/Warning';

/**
 * Card component representing a single waste collection station.
 * Shows current volume, allows volume adjustment, and collection confirmation.
 * @param {object} props - Component props
 * @param {object} props.station - Station data object
 * @param {function} props.onUpdateVolume - Callback for volume updates
 * @param {function} props.onConfirmCollection - Callback for collection confirmation
 */
const StationCard = ({ station, onUpdateVolume, onConfirmCollection }) => {
  const [sliderValue, setSliderValue] = useState(station.volume_percentage);
  const [isEditing, setIsEditing] = useState(false);

  /**
   * Determines the color for the progress bar based on fill percentage.
   * @param {number} percentage - Current fill percentage (0-100)
   * @returns {string} Color name for the progress bar
   */
  const getProgressColor = (percentage) => {
    if (percentage < 50) return 'success';
    if (percentage < 80) return 'warning';
    return 'error';
  };

  /**
   * Handles slider value changes during editing.
   * @param {object} event - React change event
   * @param {number} newValue - New slider value
   */
  const handleSliderChange = (event, newValue) => {
    setSliderValue(newValue);
  };

  /**
   * Saves the new volume value to the API and exits edit mode.
   */
  const handleSaveVolume = () => {
    onUpdateVolume(station.id, sliderValue);
    setIsEditing(false);
  };

  /**
   * Cancels editing and resets to the original volume value.
   */
  const handleCancelEdit = () => {
    setSliderValue(station.volume_percentage);
    setIsEditing(false);
  };

  return (
    <Card 
      elevation={4} 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.3s, box-shadow 0.3s',
        '&:hover': {
          transform: 'translateY(-5px)',
          boxShadow: 8,
        },
        borderLeft: station.collection_requested ? '5px solid #ff9800' : 'none',
      }}
    >
      <CardHeader
        title={station.name}
        subheader={`Última atualização: ${new Date(station.updated_at).toLocaleString()}`}
        action={
          station.collection_requested && (
            <Chip 
              icon={<WarningIcon />} 
              label="Coleta Solicitada" 
              color="warning" 
              variant="outlined"
              sx={{ fontWeight: 'bold' }}
            />
          )
        }
      />
      
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Volume Atual
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Box sx={{ flexGrow: 1, mr: 1 }}>
              <LinearProgress 
                variant="determinate" 
                value={station.volume_percentage} 
                color={getProgressColor(station.volume_percentage)}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </Box>
            <Typography variant="body2" color="text.secondary">
              {`${Math.round(station.volume_percentage)}%`}
            </Typography>
          </Box>
        </Box>
        
        {isEditing ? (
          <Box sx={{ mb: 2 }}>
            <Typography id="volume-slider" gutterBottom>
              Ajustar Volume (%)
            </Typography>
            <Slider
              value={sliderValue}
              onChange={handleSliderChange}
              aria-labelledby="volume-slider"
              valueLabelDisplay="auto"
              step={1}
              marks
              min={0}
              max={100}
            />
          </Box>
        ) : null}
      </CardContent>
      
      <CardActions sx={{ justifyContent: 'space-between', p: 2 }}>
        {isEditing ? (
          <>
            <Button 
              size="small" 
              color="primary" 
              variant="contained" 
              onClick={handleSaveVolume}
            >
              Salvar
            </Button>
            <Button 
              size="small" 
              color="error" 
              onClick={handleCancelEdit}
            >
              Cancelar
            </Button>
          </>
        ) : (
          <>
            <Button 
              size="small" 
              color="primary" 
              variant="outlined" 
              onClick={() => setIsEditing(true)}
              startIcon={<DeleteSweepIcon />}
            >
              Ajustar Volume
            </Button>
            
            {station.collection_requested && (
              <Button 
                size="small" 
                color="success" 
                variant="contained" 
                onClick={() => onConfirmCollection(station.id)}
                startIcon={<LocalShippingIcon />}
              >
                Confirmar Coleta
              </Button>
            )}
          </>
        )}
      </CardActions>
    </Card>
  );
};

export default StationCard;
