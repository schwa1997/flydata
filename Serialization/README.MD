# serializeAirportCity.py

## Overview

This script converts airport and city data from CSV files into RDF (Resource Description Framework) format using the Turtle serialization. It creates two separate TTL files: one for airports and one for cities.

## Key Components

### 1. File Paths Setup

```python
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
OUTPUT_PATH_AIRPORT = BASE_PATH / "Serialization" /"ttl"/ "airport.ttl"
OUTPUT_PATH_CITY = BASE_PATH / "Serialization" /"ttl"/ "city.ttl"
```

- Defines paths for input CSV files and output TTL files

### 2. Data Reading Functions

#### `read_cities()`

- Reads the cities CSV file using pandas
- Creates a dictionary with city_ascii as key
- Stores city name and population for each city
- Skips entries with missing city names
- Returns a dictionary of cities

#### `read_airports()`

- Reads the airports CSV file using CSV reader
- Filters for airports with IATA codes only
- Extracts airport name, city, and IATA code
- Returns a list of airport dictionaries

### 3. Main Serialization Function (`serialize_to_ttl()`)

#### Setup

- Creates two RDF graphs: one for airports and one for cities
- Defines and binds the custom namespace (FDO)
- Establishes the `isLocatedInCity` property relationship

#### City Processing

- Iterates through cities dictionary
- Creates URI for each city
- Adds triples for:
  - City type
  - City name
  - Population

#### Airport Processing

- Iterates through airports list
- Creates URI using IATA code
- Adds triples for:
  - Airport type
  - Airport name
  - Relationship to city (if city exists in dataset)

#### Output

- Serializes both graphs to separate TTL files in Turtle format

## Data Model

- Uses custom ontology (FDO namespace)
- Creates relationships between airports and cities
- Maintains separate graphs for airports and cities
