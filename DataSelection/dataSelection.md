<img src="https://www.unidformazione.com/wp-content/uploads/2018/04/unipd-universita-di-padova.png" alt="University of Padova Logo" style="float: right; width: 150px;">

# FLYDATA - Domain and Data Selection

## Table of Contents

1. [Group Information](#group-information)
2. [Selected Datasets](#selected-datasets)
3. [Model Design](#model-design)
4. [Main Challenges](#main-challenges)
5. [Main Characteristics](#main-characteristics)

## Group Information

- **Group Name:** FLYDATA
- **Group Members:**
  1. Huimin Chen - huimin.chen@studenti.unipd.it - Computer Engineering
  2. Luca Pellegrini - luca.pellegrini.5@studenti.unipd.it - Computer Engineering
  3. Nele Lauryssen - nele.lauryssen@studenti.unipd.it - Computer Science

## Selected Datasets

1. **Airports**

   - URL: [https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat)
   - Description: Comprehensive dataset containing detailed information about airports worldwide.
   - Relevance: Starting and ending points of flights; potential for analyzing airport traffic.
   - Note: Extended version available at [https://github.com/jpatokal/openflights/blob/master/data/airports-extended.dat](https://github.com/jpatokal/openflights/blob/master/data/airports-extended.dat)

2. **Aircrafts**

   - URL: [https://github.com/jpatokal/openflights/blob/master/data/planes.dat](https://github.com/jpatokal/openflights/blob/master/data/planes.dat)
   - from this [website](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download), you can download the aircraft registration dataset.
   - Description: List of planes with Name, IATA code, ICAO code. The second dataset contains more information about the aircraft such as manufacturer, type, etc.
   - Relevance: Essential for flight operations.

3. **Carriers**

   - URL: [https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat)
   - Description: List of airlines with detailed information.
   - Relevance: Flight operators; potential for performance analysis.

4. **Routes**

   - URL: [https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat)
   - Description: List of routes with comprehensive flight planning information.
   - Relevance: Connects airports; provides insights into flight planning and route popularity.

5. **Countries**

   - URL: [https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat)
   - Description: List of countries with ISO and DAFIF codes.
   - Relevance: Contextual information for airports; potential impact on flight quantity and route planning.

6. **Cities**

   - URL: [https://simplemaps.com/data/world-cities](https://simplemaps.com/data/world-cities)
   - Description: List of cities with geographic and demographic information.
   - Relevance: Context for airports; potential correlation between population and route numbers.

7. **Flights**

   - URL: [https://www.bts.gov/browse-statistical-products-and-data/bts-publications/airline-service-quality-performance-234-time](https://www.bts.gov/browse-statistical-products-and-data/bts-publications/airline-service-quality-performance-234-time)
   - Relevance: Insights into airline performance and on-time statistics.
   - Note: From this [website](https://esubmit.rita.dot.gov/On-Time-Form3A.aspx), you can check the column names of the dataset.

8. **Runways**

   - URL: [https://ourairports.com/data/](https://ourairports.com/data/)
   - Description: Detailed runway information including dimensions and characteristics.
   - Relevance: Critical for understanding airport capacity and operations.

## Model Design

![Graph Component Model](GraphComp.svg)

### Main Entities

1. Flight: flight number, departure time, arrival time, departure airport, arrival airport, route, aircraft etc.
2. Airport: name, code, etc.
3. Route: departure airport, arrival airport
4. Aircraft: name, code, etc.
5. Manufacturer: name, etc.
6. Carrier: name, code, etc.
7. Country: name, code, etc.
8. City: name, population, etc.
9. Runway: name, length, width, etc.

### Relationships

1. Route - Airport: "hasDepartureAirport"
2. Route - Airport: "hasArrivalAirport"
3. Flight - Route: "hasRoute"
4. Flight - Carrier: "isOperatedBy"
5. Aircraft - Manufacturer: "hasManufacturer"
6. Aircraft - Carrier: "isOwnedBy"
7. Route - Carrier: "hasCarrier"
8. Aircraft - Carrier: "PropertyOf"
9. Route - City: "isLocatedInCity"
10. City - Country: "isLocatedInCountry"

This model enables flexible querying and analysis, such as:

- Finding all routes from a specific airport
- Analyzing airline operations across different countries
- Exploring the relationship between city population and airport traffic

The model is extensible to include additional entities like Planes, Runways, and Delay Causes for more detailed analysis.

## Main Challenges

1. Data Integration: Combining multiple datasets with varying formats and structures.
2. Data Quality: Ensuring accuracy and completeness across all datasets.
3. Data Volume: Managing large amounts of frequently updated data.
4. Temporal Alignment: Dealing with time zone differences and aligning data from different periods.
5. Relationship Mapping: Establishing correct relationships between entities across datasets.
6. Data Cleaning: Handling missing values, duplicates, and errors in raw datasets.
7. Performance Optimization: Designing efficient queries and data structures for complex analyses.

## Main Characteristics

1. Global Coverage: Comprehensive worldwide information on air travel.
2. Multi-dimensional: Spans geographic, operational, and performance-related aspects.
3. Interconnected: Allows for complex analyses across different entities in the air travel ecosystem.
4. Wide Application: Useful for flight planning, route optimization, performance analysis, and customer service.
