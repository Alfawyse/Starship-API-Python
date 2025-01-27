# Starship API Python

Starship API Python is a FastAPI-based application designed to interact with the Star Wars API (SWAPI). The project fetches and manages data about starships and pilots while allowing users to update starship data locally. This project serves as a demonstration of clean API design, testing, and Python programming principles.

This repository is also part of a technical test, demonstrating the use of modern tools like FastAPI, Poetry, and Pytest to deliver a scalable and maintainable application.

## Project Structure

```plaintext
Starship-API-Python/
├── app/
│   ├── api/
│   │   ├── __init__.py       # Initializes the API module
│   │   ├── routes.py         # Defines the API routes
│   ├── core/
│   │   ├── __init__.py       # Initializes the core module
│   │   ├── config.py         # Handles configurations (e.g., environment variables)
│   ├── models/
│   │   ├── __init__.py       # Initializes the models module
│   │   ├── schemas.py        # Defines the Pydantic models used in the API
│   ├── services/
│   │   ├── __init__.py       # Initializes the services module
│   │   ├── swapi_service.py  # Service to interact with the SWAPI
├── tests/
│   ├── __init__.py           # Initializes the test suite
│   ├── test_pilots.py        # Unit tests for pilot-related functionality
│   ├── test_starships.py     # Unit tests for starship-related functionality
├── .gitignore                # Files to exclude from Git
├── poetry.lock               # Locked dependencies
├── pyproject.toml            # Project configuration for Poetry
├── main.py                   # Entry point for running the FastAPI app
├── README.md                 # Project documentation

```

## Installation

To get the project up and running on your local environment, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Starship-API-Python.git
    cd Starship-API-Python
    ```

2. **Install dependencies**:
    Ensure you have Poetry installed in your system. If not, install it from [here](https://python-poetry.org/docs/#installation).
    ```bash
    poetry install
    ```

3. **Activate the virtual environment**:
    ```bash
    poetry shell
    ```

4. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

5. **Access the API**:
    Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000). The Swagger documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Features

- **Fetch Starships**: Retrieve a list of starships from the Star Wars API.
- **Search Starship by Name**: Look up detailed information for a specific starship.
- **List Pilots**: Retrieve all pilots who have piloted starships, including their details.
- **Search Pilot by Name**: Find detailed information about a specific pilot.
- **Update Starships**: Update starship details in the local database.
- **Modular Design**: Clean separation of concerns with dedicated modules for routes, services, and models.


## API Documentation

The API offers several endpoints to interact with starships and pilots from the Star Wars API (SWAPI). Below is an overview of the available routes and their usage.

---

### Starships Endpoints

#### **GET /starships**
- **Description**: Retrieve a list of all available starships from the SWAPI.
- **Example Response**:
  ```json
  {
    "starships": [
      {
        "name": "X-wing",
        "model": "T-65 X-wing",
        "cost_in_credits": "149999",
        "max_atmosphering_speed": "1050"
      }
    ],
    "next": "https://swapi.py4e.com/api/starships/?page=2"
  }

---

#### **GET /starships/details/{starship_name}**
- **Description**: Fetch detailed information about a specific starship by its name.
- **Parameters**:
  - `starship_name` (string): Name of the starship to retrieve details for.


- **Example Request**:

`GET /starships/details/X-wing`

- **Example Response**:
```json
{
  "name": "X-wing",
  "model": "T-65 X-wing",
  "cost_in_credits": "149999",
  "max_atmosphering_speed": "1050",
  "crew_capacity": "1",
  "passenger_capacity": "0",
  "cargo_capacity": "110"
}
```
- **Error Response**:

```json
{
  "detail": "Starship not found"
}
```

---

#### **PUT /starships/update**
- **Description**: Update the information of a specific starship in the local database.
- **Request Body**:
  ```json
  {
    "name": "Millennium Falcon",
    "model": "YT-1300 light freighter",
    "cost_in_credits": "150000",
    "max_atmosphering_speed": "1100",
    "crew_capacity": 6,
    "passenger_capacity": 8,
    "pilots": ["Han Solo", "Chewbacca"]
  }
  
- **Example Request**:

`PUT /starships/update`

- **Example Response**:
```json
{
  "message": "Starship updated successfully",
  "data": {
    "name": "Millennium Falcon",
    "model": "YT-1300 light freighter",
    "cost_in_credits": "150000",
    "max_atmosphering_speed": "1100",
    "crew_capacity": 6,
    "passenger_capacity": 8,
    "pilots": ["Han Solo", "Chewbacca"]
  }
}

```
- **Error Response**:

```json
{
  "detail": "Starship not found"
}
```
---

### Pilots Endpoints

#### **GET /pilots**
- **Description**: Retrieve a list of pilots associated with starships.
- **Example Request**:

`GET /pilots`

- **Example Response**:
```json
{
  "pilots": [
    {
      "name": "Luke Skywalker",
      "height": "172",
      "gender": "male",
      "weight": "77",
      "birth_year": "19BBY",
      "species_name": "Human",
      "starships": ["X-wing"],
      "homeworld": "Tatooine"
    }
  ]
}
```
- **Error Response**:

```json
{
  "error": "Failed to fetch pilots."
}
```
---

#### **GET /pilots/details/{pilot_name}**
- **Description**:  Retrieve detailed information about a specific pilot by name.
- **Example Request**:

`GET /pilots/details/Luke Skywalker`

- **Example Response**:
```json
{
  "name": "Luke Skywalker",
  "height": "172",
  "gender": "male",
  "weight": "77",
  "birth_year": "19BBY",
  "species_name": "Human",
  "starships": [
    {
      "name": "X-wing",
      "model": "T-65 X-wing"
    }
  ],
  "homeworld": "Tatooine"
}

```
- **Error Response**:

```json
{
  "error": "Pilot not found or has no starships."
}
```
---
### Error Handling Overview

The API includes robust error handling with clear messages for common issues:

#### **Resource Not Found**
- **Status Code**: 404
- **Response**:
```json
{
  "detail": "Resource not found"
}
```
#### **SWAPI Connection Issues**
- **Status Code**: 500
- **Response**:
```json
{
  "error": "Failed to connect to SWAPI."
}
```

#### **Unexpected Errors**
- **Status Code**: 500
- **Response**:
```json
{
  "error": "An unexpected error occurred."
}
```

---

## Testing

This project includes a suite of tests to ensure the application works as expected. The tests cover various functionalities such as fetching data from the SWAPI, handling errors, and updating the local database.

### Run Tests
To execute the test suite, run the following command:
```bash
poetry run pytest
```

### Test Structure
The tests are organized as follows:

- tests/test_starships.py: Contains tests related to starship endpoints, including:

  - Fetching all starships.
  - Fetching a specific starship by name.
  - Handling errors from the SWAPI for starships.
  - Updating a starship in the local database.
  
- tests/test_pilots.py: Contains tests related to pilot endpoints, including:

  - Fetching all pilots with starships.
  - Fetching a specific pilot by name.
  - Handling errors from the SWAPI for pilots.

### Example Output

After running the test suite, you should see output similar to this:

```bash
======================================================================================================= test session starts =======================================================================================================
platform win32 -- Python 3.11.9, pytest-7.4.4, pluggy-1.5.0
collected 10 items                                                                                                                                                                                                             

tests/test_starships.py ....                                                                                                                                                                                            [ 40%]
tests/test_pilots.py ....                                                                                                                                                                                               [100%]

======================================================================================================= 10 passed in 2.34s =======================================================================================================
```
### Test Coverage

To check how much of your code is covered by the tests, you can use `pytest-cov`. Install it with the following command:

```bash
poetry add pytest-cov --dev
poetry run pytest --cov=app
```
### Example Output

```bash
---------- coverage: platform win32, python 3.11.9 ----------
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
app/api/routes.py                         32      0   100%
app/models/schemas.py                     10      0   100%
app/services/swapi_service.py             50      0   100%
tests/test_pilots.py                      15      0   100%
tests/test_starships.py                   20      0   100%
----------------------------------------------------------
TOTAL                                    127      0   100%
================== 10 passed in 2.34s =====================
```

This indicates 100% test coverage, meaning all lines of code are tested. Adjust as necessary based on actual coverage.

---

## Future Improvements

### Expand API Endpoints:

- Add more endpoints to cover additional resources available from the SWAPI.

### Enhanced Caching:

- Implement caching mechanisms to reduce repeated SWAPI calls and improve response times.

### Improve Error Handling:

- Add more granular error messages for specific scenarios, such as timeouts or rate limits from SWAPI.

### Authentication:

- Secure the API with authentication mechanisms like OAuth2 or API keys.

### Dockerization:

- Provide a Dockerfile and compose setup for easier deployment and testing.

---
### Acknowledgments

This project is built using the [Star Wars API (SWAPI)](https://swapi.py4e.com/), which provides open access to data from the Star Wars universe. Special thanks to the maintainers of SWAPI for this amazing resource.
