# B2Blue Challenge - Storage Volume Control System

## Overview
This system was developed for B2Blue to manage waste storage volume control. It monitors storage station occupancy levels, automatically generates collection requests when volume reaches 80%, and maintains a complete operation history.

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation Options](#installation-options)
  - [Accessing the Application](#accessing-the-application)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [REST API Documentation](#rest-api-documentation)
  - [Stations API](#stations-api)
  - [History API](#history-api)
  - [API Examples](#api-examples)
- [Data Structure](#data-structure)
- [Operation Flow](#operation-flow)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Security Features](#security-features)
- [Future Extensions](#future-extensions)

## Quick Start
### Prerequisites
- Python: 3.12^
- Node.js: 23.10.0

### Installation Options

#### Option 1: Docker Compose (Recommended)
```sh
git clone git@github.com:luizpbraga/Desafio-B2Blue.git
cd Desafio-B2Blue
docker-compose up --build
```

#### Option 2: Manual Setup
**Backend (Django)**
```bash
cd Desafio-B2Blue/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_initial_data
python manage.py runserver
```

**Frontend (React)**
```sh
cd Desafio-B2Blue/frontend
npm install
npm start
```

### Accessing the Application
- **Frontend**: <http://localhost:3000>
- **Backend**: <http://localhost:8000>
- **API Root**: <http://localhost:8000/api/>
- **Admin Interface**: <http://localhost:8000/admin/>

## Key Features
1. **Station Management**
   - Monitor real-time status of all storage stations
   - Adjust volume levels via intuitive interface
   - Visual indicators for stations requiring collection

2. **Automatic Collection Requests**
   - System generates collection requests when stations reach 80% capacity
   - Clear visual highlighting of stations awaiting collection

3. **Collection Workflow**
   - One-click collection confirmation
   - Automatic volume reset after collection
   - Complete audit trail of all operations

4. **Operation History**
   - Comprehensive log of all system activities
   - Filter history by station

## System Architecture
The application follows a client-server architecture:
- **Backend**: Django REST Framework API handling business logic and data persistence
- **Frontend**: React application with Material UI components for user interaction

## REST API Documentation

### Stations API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stations/` | GET | List all stations |
| `/api/stations/` | POST | Create a new station |
| `/api/stations/{id}/` | GET | Get station details |
| `/api/stations/{id}/` | PATCH | Update station partially |
| `/api/stations/{id}/` | PUT | Update station completely |
| `/api/stations/{id}/` | DELETE | Delete a station |
| `/api/stations/{id}/confirm_collection/` | POST | Confirm waste collection |

### History API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/history/` | GET | List all history records (supports filtering) |
| `/api/history/{id}/` | GET | Get specific history record |

### API Examples

#### Create Station
```http
POST /api/stations/
Content-Type: application/json

{
  "name": "Estação D",
  "volume_percentage": 30.5
}
```

Response:
```json
{
  "id": 4,
  "name": "Estação D",
  "volume_percentage": 30.5,
  "collection_requested": false,
  "created_at": "2025-04-13T15:20:33.123456Z",
  "updated_at": "2025-04-13T15:20:33.123456Z"
}
```

#### Update Station Volume
```http
PATCH /api/stations/1/
Content-Type: application/json

{
  "volume_percentage": 85.0
}
```

Response:
```json
{
  "id": 1,
  "name": "Estação A",
  "volume_percentage": 85.0,
  "collection_requested": true,
  "created_at": "2025-04-10T13:45:22.123456Z",
  "updated_at": "2025-04-13T15:30:12.654321Z"
}
```

#### Confirm Collection
```http
POST /api/stations/1/confirm_collection/
```

Response:
```json
{
  "success": true,
  "message": "Coleta confirmada com sucesso.",
  "station": {
    "id": 1,
    "name": "Estação A",
    "volume_percentage": 0.0,
    "collection_requested": false,
    "created_at": "2025-04-10T13:45:22.123456Z",
    "updated_at": "2025-04-13T15:35:47.123456Z"
  }
}
```

#### Get Filtered History
```http
GET /api/history/?station_id=1
```

Response (abbreviated):
```json
{
  "count": 3,
  "results": [
    {
      "id": 15,
      "station": 1,
      "station_name": "Estação A",
      "operation_type": "collection_complete",
      "volume_percentage": 0.0,
      "timestamp": "2025-04-13T15:35:47.123456Z",
      "notes": "Coleta confirmada. Volume anterior: 85.0%"
    },
    ...
  ]
}
```

#### Error Handling Example
```http
POST /api/stations/2/confirm_collection/
```

Response (400 Bad Request):
```json
{
  "error": "Não há pedido de coleta para esta estação."
}
```

## Data Structure

### Main Models

1. **Station**
   - `name`: Station identifier
   - `volume_percentage`: Current volume (0-100%)
   - `collection_requested`: Collection status flag
   - `created_at`/`updated_at`: Timestamps

2. **StationHistory**
   - `station`: Reference to the station
   - `operation_type`: Action performed ('create', 'update', 'collection_request', 'collection_complete')
   - `volume_percentage`: Volume at time of operation
   - `timestamp`: When the operation occurred
   - `notes`: Operation details

## Operation Flow
1. Dashboard shows current station status
2. User adjusts volume with slider
3. System automatically flags stations at ≥80% for collection
4. User confirms collection when completed
5. System resets volume to zero and logs the operation
6. Complete history is available for review

## Testing
Run the automated test suite:
```bash
cd backend
python manage.py test
```

The tests cover:
- Data validation
- API endpoints
- Business logic
- Data integrity

## Technologies Used

### Backend
- Django 5.2
- Django REST Framework 3.16
- SQLite (database)

### Frontend
- React
- Material UI
- Axios

## Security Features
- Backend data validation
- CSRF protection
- CORS configuration

## Future Extensions
- User authentication and permissions
- Multiple waste types per station
- Collection scheduling
- Analytics dashboard