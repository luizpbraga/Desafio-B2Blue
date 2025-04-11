# B2Blue Challenge
Storage Volume Control System

## Overview
This system was developed for B2Blue with the objective of managing waste storage volume control. It allows monitoring the occupancy level of storage stations, automatically generating collection requests when the volume reaches 80%, and recording the entire history of operations.

## Table of Contents
1. [Technologies Used](#technologies-used)
   - [Backend](#backend)
   - [Frontend](#frontend)
2. [System Architecture](#system-architecture)
3. [Data Structure](#data-structure)
   - [Main Models](#main-models)
4. [Key Features](#key-features)
5. [Operation Flow](#operation-flow)
6. [REST API](#rest-api)
7. [Security](#security)
8. [Prerequisites](#prerequisites)
9. [Installation and Execution](#installation-and-execution-instructions)
   - [Docker Compose](#build-with-docker-compose)
   - [Backend Setup](#backend-django)
   - [Frontend Setup](#frontend-react)
   - [Accessing the Application](#accessing-your-application)
10. [Final Considerations](#final-considerations)

## Technologies Used
### Backend
- Django: Python web framework for rapid development  
- Django REST Framework: Extension for creating RESTful APIs  
- SQLite: Relational database for data storage  

### Frontend
- React: JavaScript library for building interfaces  
- Material UI: React component framework for consistent design  
- Axios: HTTP client for API communication  

## System Architecture
The system follows a client-server architecture divided into two parts:  
    1. Backend (Django): Handles business logic, data persistence, and exposes the REST API  
    2. Frontend (React): User interface that consumes the API to display and manipulate data  

## Data Structure
### Main Models

1. Station  
    - Attributes:  
        - name: Station name  
        - volume_percentage: Occupied volume percentage (0-100%)  
        - collection_requested: Flag indicating if there is a pending collection request  
        - created_at: Creation date/time  
        - updated_at: Last update date/time  

2. StationHistory  
    - Attributes:  
        - station: Reference to the station (foreign key)  
        - operation_type: Type of operation ('create', 'update', 'collection_request', 'collection_complete')  
        - volume_percentage: Volume percentage at the time of the operation  
        - timestamp: Operation date/time  
        - notes: Notes about the operation  

## Key Features

1. Station Management  
    - View the current status of all stations  
    - Adjust the volume of each station  
    - Visual identification of stations with pending collection requests  

2. Automatic Collection Request Generation  
    - When a station reaches or exceeds 80% occupancy, a collection request is automatically generated  
    - Stations with collection requests are visually highlighted  

3. Collection Confirmation  
    - Users can confirm that the collection has been completed  
    - After confirmation, the station's volume is automatically reset to zero  

4. Complete Operation History  
    - All operations are recorded in the history  
    - The history can be viewed in full or filtered by station  

## Operation Flow
- The user views the current status of the stations on the dashboard  
- The user can adjust a station's volume using the slider  
- If the updated volume reaches 80% or more, the system automatically generates a collection request  
- With a pending collection request, the "Confirm Collection" button becomes available  
- Clicking the confirmation button records the collection and resets the station's volume to zero  
- All these operations are recorded in the history at the bottom of the screen  

## REST API
The API follows RESTful principles and uses standard HTTP formats for communication:  
- Read requests use the GET method  
- Creations use POST  
- Updates use PUT or PATCH  
- Deletions use DELETE  
- Data is transferred in JSON format  

## Security
The system implements:  
- Backend data validation  
- CSRF protection for POST requests  
- CORS configuration to allow only the frontend to access the API  

## Prerequisites
- Python: 3.8+
- node: 23.10.0

## Installation and Execution Instructions
First, clone the repository: 
```sh
    git clone git@github.com:luizpbraga/Desafio-B2Blue.git
```
### Build with Docker Compose
```sh
cd Desafio-B2Blue
docker-compose up --build
```
see [Accessing Your Application](#accessing-your-application) after build completes.

### Backend (Django)
1. Go to folder
```bash
cd Desafio-B2Blue/backend
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create initial data (stations)
```bash
python manage.py setup_initial_data
```

6. Run the development server
```bash
python manage.py runserver
```
### Frontend (React)
1 Navegate to the frontend folder
```sh
cd Desafio-B2Blue/frontend
```
2. Install dependencies
```sh
npm install
```
3. Run the development server
```sh
npm start
```
### Accessing Your Application
- **Frontend**: <http://localhost:3000>
- **Backend**: <http://localhost:8000>

## Final Considerations
This project implements all the requirements specified in the B2Blue challenge, focusing on structured communication between frontend and backend through a REST API using Django REST Framework. The user interface is responsive and follows modern design principles with Material UI.
