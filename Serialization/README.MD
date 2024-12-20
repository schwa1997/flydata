<img src="https://www.unidformazione.com/wp-content/uploads/2018/04/unipd-universita-di-padova.png" alt="University of Padova Logo" style="float: right; width: 150px;">

# FLYDATA - RDF Dataset Documentation

## Table of Contents

1. [Basic Information](#basic-information)
2. [Task Objective](#task-objective)
3. [Dataset Information](#dataset-information)
4. [RDF Model](#rdf-model)
5. [Technical Implementation](#technical-implementation)
6. [RDF Statistics](#rdf-statistics)

## Basic Information

### Group Information

- **Group Name:** FLYDATA
- **Group Members:**
  1. Huimin Chen - huimin.chen@studenti.unipd.it - Computer Engineering
  2. Luca Pellegrini - luca.pellegrini.5@studenti.unipd.it - Computer Engineering
  3. Nele Lauryssen - nele.lauryssen@studenti.unipd.it - Computer Science

### Repository Access

The complete RDF dataset is available in Turtle format at our [GitHub Repository](https://github.com/schwa1997/flydata/tree/main/Serialization/ttl)

## Task Objective

Our primary objective is to transform diverse aviation-related CSV datasets into a semantically rich RDF format. This transformation aims to:

- Create meaningful connections between different aviation entities (airports, flights, carriers, etc.)
- Preserve data integrity and relationships during the conversion process
- Establish a standardized ontology for aviation data
- Enable semantic querying and knowledge discovery
- Ensure data interoperability through standard RDF representations

## Dataset Information

### Dataset Statistics

| Dataset           | Entities | Properties | Column Names |
| ----------------- | -------- | ---------- | -------------------------- |
| States.csv        | 52       | 2          | State, Abbreviation |
| Cities.csv        | 31,120   | 17         | city, city_ascii, state_id, state_name, county_fips, county_name, lat, lng, population, density, source, military, incorporated, timezone, ranking, zips, id |
| Airports.csv      | 1,512    | 14         | ID, Name, City, Country, IATA, ICAO, LAT, LONG ...   |
| Carriers.csv      | 1,498    | 8          | AirlineID, Name, Alias, IATA, ICAO, Callsign, Country, Active |
| Aircraft.csv      | 299,689  | 4          | AircraftID, ModelCode, AircraftType, RegisterCity  |
| Models.csv        | 92,339   | 2          | ModelCode, ModelName |
| Manufacturers.csv | 92,339   | 2          | ManufactureCode, ManufacturerName|
| Routes.csv        | 67,663   | 9          | Airline, Airline ID, Source airport, Source airport ID, Destination airport, Destination airport ID, Codeshare, stops, Equipment  |
| Flights.csv       | 552,218  | 23         |  |

## RDF Model

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

### Data Processing Pipeline

1. **Data Selection and Scope**

   - Flight data: August 2024, US domestic flights only
   - Geographic scope: US cities and states
   - Aircraft data: FAA-registered aircraft only ([FAA Registry Database](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download))
   - Weather data: US locations, August 1-31, 2024

2. **Data Cleaning Steps**

   - Removal of duplicate entries
   - Format standardization
   - Range validation
   - Removal of records with missing critical fields

3. **Format Standardization**
   - Source formats: CSV, TXT, XLSX
   - Target format: CSV (intermediate)
   - Final format: RDF/TTL

### RDF Implementation

1. **File Structure**

```python
BASE_PATH = 'your_base_path'
DATA_PATH = BASE_PATH / "DataCollection" / "CSVData"
OUTPUT_PATH = BASE_PATH / "Serialization" / "ttl"

# Input files examples
AIRPORTS_PATH = DATA_PATH / "airports.csv"
CITIES_PATH = DATA_PATH / "cities.csv"

# Output files examples
OUTPUT_PATH_AIRPORT = OUTPUT_PATH / "airport.ttl"
OUTPUT_PATH_CITY = OUTPUT_PATH / "city.ttl"
```

2. **Configuration Details**

   - **Ontology Base URI**: `http://www.semanticweb.org/nele/ontologies/2024/10/flydata/`
   - **Output Format**: Turtle (.ttl)
   - **Implementation**: Python-based CSV-to-RDF conversion scripts

3. **Core Processing Functions**

   ```python
   def read_data(file_path: Path) -> pd.DataFrame:
       """Reads and validates source CSV data"""
       #read the aircrafts
         aircrafts = []
         try:
            with open(AIRCRAFT_PATH, 'r', encoding='utf-8') as file:
               reader = csv.DictReader(file)
               for row in reader:
                     aircrafts.append({
                        'n_number': row['AircraftID'],
                        'model_code': row['ModelCode'].strip(),
                        'aircraft_type': row['AircraftType'].strip(),
                        'register_city': row['RegisterCity'].strip()
                     })
         except Exception as e:
            print(f"Error reading aircrafts file: {str(e)}")
            raise

   def serialize_to_ttl(graph: RDFGraph, output_path: Path):
       """Exports RDF graph to Turtle format"""
       #serialization of the aircrafts and match with models to build the hasModel relationship
      index = 0
      for aircraft in aircrafts:
            encoded_n_number = quote(aircraft['n_number'].strip())
            aircraft_uri = FDO[encoded_n_number]
            g_aircraft.add((aircraft_uri, RDF.type, FDO.Aircraft))
            g_aircraft.add((aircraft_uri, FDO.aircraftType, Literal(aircraft['aircraft_type'], datatype=XSD.string)))

            for model in models:
               if aircraft['model_code'] == model['model_code']:
                     model_code = aircraft['model_code']
                     model_uri = FDO[model_code]
                     g_aircraft.add((aircraft_uri, FDO.hasModel, model_uri))
            print(f"{int(index/len(aircrafts)*100)} % complete \r", end="")
            index+=1

         print(f"serialization \r")
         g_aircraft.serialize(destination=str(OUTPUT_AIRCRAFT_PATH), format='turtle')
   ```

```

## RDF Statistics

### Dataset Overview

- Uses custom ontology (FDO namespace)
- Maintains separate graphs for different entity types
- Creates semantic relationships between entities
- Serializes data in Turtle format

### Entity Statistics

| Dataset           | Entities | Property Count | Property Names   |
| ----------------- | -------- | -------------- | ----------------------------------------- |
| States.ttl        | 52       | 2              | abbreviation, name |
| Cities.ttl        | 31,120   | 4              | name, population, isLocatedInState |
| Airports.ttl      | 1,512    | 2              | name, isLocatedInCity |
| Carriers.ttl      | 1,498    | 2              | name, callSign|
| Aircraft.ttl      | 299,689  | 2              | aircraftType, hasModel  |
| Models.ttl        | 92,339   | 2              | name, hasManufacturer |
| Manufacturers.ttl | 92,339   | 2              | name|
| Weather.ttl       | 647,458  | 3              | hasAirport, weatherDate, weatherType|
| Flights.ttl       | 552,218  | 23             | hasAircraft, hasRoute, isOperatedBy, ActualArrivalDelayTime, ActualDepartureDelayTime, ActualElapsedTimeDifference, ActualGate-to-gateTime, ActualGateArrivalTime, ActualGateDepartureTime, ActualWheels-offTime, ActualWheels-onTime, LateE, LateF, LateG, LateH, LateI, ScheduledArrivalTimePerCRS, ScheduledArrivalTimePerOAG, ScheduledDepartureCRSTime, ScheduledDepartureOAGTime, ScheduledElapsedTimePerCRS, flightDate |
| Routes.ttl        | 67,663   | 4              | hasDepartureAirport, hasArrivalAirport, hasCarrier |

### statistics of the RDF file

| TTL               | Entities |
| ----------------- | -------- |
| States.ttl        | 52       |
| Cities.ttl        | 31,120   |
| Airports.ttl      | 1,512    |
| Carriers.ttl      | 1,498    |
| Aircraft.ttl      | 299,689  |
| Models.ttl        | 92,339   |
| Manufacturers.ttl | 92,339   |
| Flights.ttl       | 552,218  |
| Routes.ttl        | 67,663   |
| Weather.ttl       | 647.458  |

### RDF Import Statistics in GraphDB

| Dataset           | Import Time | Statement Count |
| ----------------- | ----------- | --------------- |
| Weather.ttl       | 29s         | 2,589,832       |
| States.ttl        | <1s         | 156             |
| Routes.ttl        | <1s         | 27,986          |
| Models.ttl        | 6s          | 369,356         |
| Manufacturers.ttl | 2s          | 134,606         |
| Cities.ttl        | 2s          | 186,720         |
| Carriers.ttl      | <1s         | 4,017           |
| Airports.ttl      | <1s         | 6,085           |
| Aircraft.ttl      | 10s         | 899,067         |
| Flights.ttl       | >10s        | 14,789,917      |
```
