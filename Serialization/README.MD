<img src="https://www.unidformazione.com/wp-content/uploads/2018/04/unipd-universita-di-padova.png" alt="University of Padova Logo" style="float: right; width: 150px;">

# FLYDATA - RDF Dataset Documentation

## Table of Contents

1. [Group Information](#group-information)
2. [Project Overview](#project-overview)
3. [Dataset Information](#dataset-information)
4. [Technical Implementation](#technical-implementation)
5. [Data Model](#data-model)
6. [Repository Access](#repository-access)

## Group Information

- **Group Name:** FLYDATA
- **Group Members:**
  1. Huimin Chen - huimin.chen@studenti.unipd.it - Computer Engineering
  2. Luca Pellegrini - luca.pellegrini.5@studenti.unipd.it - Computer Engineering
  3. Nele Lauryssen - nele.lauryssen@studenti.unipd.it - Computer Science

## Project Overview

This project involves transforming flight-related data into RDF format using a systematic approach that preserves relationships while ensuring semantic clarity. The result is a rich, interconnected graph of aviation data.

## Dataset Information

### Dataset Statistics

| Dataset       | Entities | Properties |
| ------------- | -------- | ---------- |
| States        | 52       | 2          |
| Cities        | 31,120   | 17         |
| Airports      | 1,512    | 14         |
| Carriers      | 1,498    | 8          |
| Aircraft      | 299,689  | 4          |
| Models        | 92,339   | 2          |
| Manufacturers | 92,339   | 2          |

### Core RDF Classes and Relations

**Primary Entities**:

- Manufacturers
- Models
- Aircrafts
- Carriers
- Airports
- Cities
- States
- Flights
- Routes
- Weather

**Key Relationships**:

```turtle
airport isLocatedInCity city
route hasDepartureAirport airport
route hasArrivalAirport airport
route hasCarrier carrier
aircraft hasModel model
city isLocatedInState state
flight isOperatedBy carrier
flight hasAircraft aircraft
flight hasRoute route
model hasManufacturer manufacturer
weather hasAirport airport
```

## Technical Implementation

### Configuration

- **Ontology Namespace**: `http://www.semanticweb.org/nele/ontologies/2024/10/flydata/`
- **Format**: Turtle (.ttl)
- **Implementation**: Custom Python scripts for CSV-to-RDF transformation

### Key Components

1. **File Structure**

```python
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
OUTPUT_PATH_AIRPORT = BASE_PATH / "Serialization" /"ttl"/ "airport.ttl"
OUTPUT_PATH_CITY = BASE_PATH / "Serialization" /"ttl"/ "city.ttl"
```

2. **Data Processing Functions**

- `read_cities()`: Processes city data from CSV
- `read_airports()`: Processes airport data from CSV
- `serialize_to_ttl()`: Converts data to RDF format

## Data Model

- Uses custom ontology (FDO namespace)
- Maintains separate graphs for different entity types
- Creates semantic relationships between entities
- Serializes data in Turtle format

## Repository Access

The complete RDF dataset is available in Turtle format at our [GitHub Repository](https://github.com/schwa1997/flydata/tree/main/Serialization/ttl)
