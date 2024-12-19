import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

# Define all paths
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
STATE_PATH = BASE_PATH / "DataCollection" / "CSVData" / "states.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CARRIERS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "carriers.csv"
#ROUTES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "routes.csv"
AIRCRAFT_PATH = BASE_PATH / "DataCollection" / "CSVData" / "aircrafts.csv"
MODEL_PATH = BASE_PATH / "DataCollection" / "CSVData" / "model.csv"
MANUFACTURER_PATH = BASE_PATH / "DataCollection" / "CSVData" / "manufacturer.csv"
# Output paths
OUTPUT_PATH_AIRPORT = BASE_PATH / "Serialization" /"ttl"/ "airports.ttl"
OUTPUT_PATH_CARRIER = BASE_PATH / "Serialization" / "ttl" / "carriers.ttl"
OUTPUT_PATH_STATE = BASE_PATH / "Serialization" /"ttl"/ "states.ttl"
OUTPUT_PATH_CITY = BASE_PATH / "Serialization" /"ttl"/ "cities.ttl"
OUTPUT_PATH_AIRCRAFT = BASE_PATH / "Serialization" /"ttl"/ "aircrafts.ttl"
OUTPUT_PATH_MODEL = BASE_PATH / "Serialization" /"ttl"/ "model.ttl"
OUTPUT_PATH_MANUFACTURER = BASE_PATH / "Serialization" /"ttl"/ "manufacturer.ttl"

def read_cities():
    try:
        cities_df = pd.read_csv(CITIES_PATH)
        cities = {}
        for _, row in cities_df.iterrows():
            if pd.isna(row['city_ascii']):
                continue
                
            city_ascii = str(row['city_ascii'])
            cities[city_ascii] = {
                'name': row['city'],
                'population': str(row['population']) if pd.notna(row['population']) else "0",
                'state_id': str(row['state_id']) if pd.notna(row['state_id']) else ""  # Add state_id
            }
                    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        raise

    return cities

def read_states():
    states = []
    try:
        with open(STATE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['State'] and row['Abbreviation']:  # Need both fields
                    state_dict = {
                        'name': row['State'].strip(),
                        'abbreviation': row['Abbreviation'].strip()
                    }
                    states.append(state_dict)
    except Exception as e:
        print(f"Error reading states file: {str(e)}")
        raise
    return states
# not needed because we are popularing routes from flights
'''
def read_routes():
    routes = []
    try:
        with open(ROUTES_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                routes.append({
                    'airline': row['\ufeff"Airline"'].strip('"'),  # Added strip('"') and kept the exact column name
                    'source_airport': row['Source airport'],
                    'destination_airport': row['Destination airport']
                })
    except Exception as e:
        print(f"Error reading routes file: {str(e)}")
        raise
    return routes
'''

def read_manufacturer():
    manufacturer = []
    try:
        with open(MANUFACTURER_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                manufacturer.append({
                    'manufacture_code': row['ManufactureCode'].strip(),
                    'manufacturer_name': row['ManufacturerName'].strip()
                })
    except Exception as e:
        print(f"Error reading manufacturer file: {str(e)}")
        raise
    return manufacturer
def read_carriers():
    carriers = []
    try:
        with open(CARRIERS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['IATA']:  # Only include carriers with IATA code
                    carriers.append({
                        'name': row['Name'].strip('"'),
                        'iata': row['IATA'].strip('"'),
                        'callsign': row['Callsign'].strip('"'),
                        'airline_id': row['\ufeffAirlineID'].strip('"')  # Updated to match exact column name with BOM
                    })
    except Exception as e:
        print(f"Error reading carriers file: {str(e)}")
        raise
    return carriers
def read_airports():
    airports = []
    try:
        with open(AIRPORTS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['IATA']:  # Only include airports with IATA code
                    airports.append({
                        'name': row['Name'].strip('"'),
                        'city': row['City'].strip('"'),
                        'iata': row['IATA'].strip('"')
                    })
    except Exception as e:
        print(f"Error reading airports file: {str(e)}")
        raise
    return airports
def read_aircrafts():
    aircrafts = []
    try:
        with open(AIRCRAFT_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                aircrafts.append({
                    'n_number': row['AircraftID'],
                    'model_code': row['ModelCode'].strip()
                })
    except Exception as e:
        print(f"Error reading aircrafts file: {str(e)}")
        raise
    return aircrafts
def read_model():
    model = []
    try:
        with open(MODEL_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.append({
                    'model_code': row['ModelCode'].strip(),
                    'model_name': row['ModelName'].strip()
                })
    except Exception as e:
        print(f"Error reading model file: {str(e)}")
        raise
    return model
def serialize_to_ttl():
    # Create RDF graphs
    g_state = Graph()
    g_city = Graph()
    g_airport = Graph()
    g_carrier = Graph()
    g_aircraft = Graph()
    g_model = Graph()
    g_manufacturer = Graph()
    
    # Define namespaces
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    
    # Bind namespaces for all graphs
    for g in [g_state, g_city, g_airport, g_carrier, g_aircraft, g_model, g_manufacturer]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)
    
    # Add carrier properties
    g_carrier.add((FDO.hasRoute, RDF.type, RDF.Property))
    g_carrier.add((FDO.hasRoute, RDFS.domain, FDO.Carrier))
    g_carrier.add((FDO.callSign, RDF.type, RDF.Property))
    g_carrier.add((FDO.callSign, RDFS.domain, FDO.Carrier))
    
    # Define properties
    g_city.add((FDO.isLocatedInState, RDF.type, RDF.Property))
    g_city.add((FDO.isLocatedInState, RDFS.domain, FDO.City))
    g_city.add((FDO.isLocatedInState, RDFS.range, FDO.State))

    
    
    states = read_states()
    cities = read_cities()
    carriers = read_carriers()
    # not needed because we are popularing routes from flights
    #routes = read_routes()
    airports = read_airports()
    aircrafts = read_aircrafts()
    model = read_model()
    manufacturer = read_manufacturer()
    # Create a mapping of state abbreviations to URIs
    state_uri_mapping = {
        state['abbreviation']: URIRef(str(FDO) + quote(state['name'].replace(" ", "_"))) 
        for state in states
    }
    
    # Add cities to the city graph
    for city_ascii, data in cities.items():
        city_id = quote(city_ascii.encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
        city_uri = URIRef(str(FDO) + city_id)
        
        # Add city triples
        g_city.add((city_uri, RDF.type, FDO.City))
        g_city.add((city_uri, FDO.name, Literal(data['name'], datatype=XSD.string)))
        g_city.add((city_uri, FDO.population, Literal(data['population'], datatype=XSD.string)))
        
        # Add relationship to state if state_id exists
        if data['state_id']:  # Check if state_id exists and is not empty
            state_abbrev = data['state_id']
            if state_abbrev in state_uri_mapping:
                state_uri = state_uri_mapping[state_abbrev]
                g_city.add((city_uri, FDO.isLocatedInState, state_uri))

    # Add states to the state graph
    for state in states:
        state_uri = state_uri_mapping[state['abbreviation']]
        g_state.add((state_uri, RDF.type, FDO.State))
        g_state.add((state_uri, FDO.name, Literal(state['name'], datatype=XSD.string)))

    # Serialize both graphs to separate TTL files
    g_state.serialize(destination=str(OUTPUT_PATH_STATE), format='turtle')
    g_city.serialize(destination=str(OUTPUT_PATH_CITY), format='turtle')

    # Define the isLocatedInCity property in the airport graph
    g_airport.add((FDO.isLocatedInCity, RDF.type, RDF.Property))
    g_airport.add((FDO.isLocatedInCity, RDFS.domain, FDO.Airport))
    g_airport.add((FDO.isLocatedInCity, RDFS.range, FDO.City))

    # Add cities to the city graph
    for city_ascii, data in cities.items():
        # Remove special characters and spaces, then URL encode
        city_id = quote(city_ascii.encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
        city_uri = URIRef(str(FDO) + city_id)
        
        # Add city triples
        g_city.add((city_uri, RDF.type, FDO.City))
        g_city.add((city_uri, FDO.name, Literal(data['name'], datatype=XSD.string)))
        g_city.add((city_uri, FDO.population, Literal(data['population'], datatype=XSD.string)))

    # Add airports and their relationships to the airport graph
    for airport in airports:
        # Use IATA code directly in the URI
        airport_uri = URIRef(str(FDO) + airport['iata'])
        
        # Add airport triples
        g_airport.add((airport_uri, RDF.type, FDO.Airport))
        g_airport.add((airport_uri, FDO.name, Literal(airport['name'], datatype=XSD.string)))
        
        # Only add isLocatedInCity if the city exists in our cities dataset
        if airport['city'] in cities:
            city_id = quote(airport['city'].encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
            city_uri = URIRef(str(FDO) + city_id)
            g_airport.add((airport_uri, FDO.isLocatedInCity, city_uri))

    # Serialize both graphs to separate TTL files
    g_airport.serialize(destination=str(OUTPUT_PATH_AIRPORT), format='turtle')
    g_city.serialize(destination=str(OUTPUT_PATH_CITY), format='turtle')

    # Fix carrier serialization (proper indentation and using g_carrier)
    for carrier in carriers:
        carrier_uri = FDO[carrier['iata']]
        g_carrier.add((carrier_uri, RDF.type, FDO.Carrier))
        g_carrier.add((carrier_uri, RDFS.label, Literal(carrier['name'], datatype=XSD.string)))
        g_carrier.add((carrier_uri, FDO.callSign, Literal(carrier['callsign'], datatype=XSD.string)))
        # Add routes for this carrier
        # not needed because we are popularing routes from flights
        '''
        for route in routes:
            if route['airline'] == carrier['iata']:
                route_uri = FDO[f"{route['source_airport']}{route['destination_airport']}"]
                g_carrier.add((carrier_uri, FDO.hasRoute, route_uri))
        '''

    # Define hasModel property
    g_aircraft.add((FDO.hasModel, RDF.type, RDF.Property))
    g_aircraft.add((FDO.hasModel, RDFS.domain, FDO.Aircraft))
    g_aircraft.add((FDO.hasModel, RDFS.range, FDO.Model))

    # Create model mappings and add model data first
    model_uri_mapping = {}
    for model_data in model:
        model_uri_mapping[model_data['model_code']] = URIRef(str(FDO) + quote(model_data['model_code']))

    # Aircraft serialization
    for aircraft in aircrafts:
        # Properly encode the N-number for the URI
        encoded_n_number = quote(aircraft['n_number'].strip())
        aircraft_uri = FDO[encoded_n_number]
        g_aircraft.add((aircraft_uri, RDF.type, FDO.Aircraft))
        g_aircraft.add((aircraft_uri, FDO.name, Literal(aircraft['n_number'], datatype=XSD.string)))
        
        if aircraft['model_code']:
            model_code = aircraft['model_code']
            model_uri = model_uri_mapping[model_code]
            g_aircraft.add((aircraft_uri, FDO.hasModel, model_uri))
  
    for model_data in model:
        model_uri = model_uri_mapping[model_data['model_code']]
        g_model.add((model_uri, RDF.type, FDO.Model))
        g_model.add((model_uri, FDO.name, Literal(model_data['model_name'], datatype=XSD.string)))
        g_model.add((model_uri, FDO.modelCode, Literal(model_data['model_code'], datatype=XSD.string)))
        g_model.add((model_uri, FDO.hasManufacturer, manufacturer_uri))

        
    g_model.add((FDO.hasManufacturer, RDF.type, RDF.Property))
    g_model.add((FDO.hasManufacturer, RDFS.domain, FDO.Model))
    g_model.add((FDO.hasManufacturer, RDFS.range, FDO.Manufacturer))
   
    for manufacturer in manufacturer:
        manufacturer_uri = FDO[manufacturer['manufacture_code']]
        g_manufacturer.add((manufacturer_uri, RDF.type, FDO.Manufacturer))
        g_manufacturer.add((manufacturer_uri, FDO.name, Literal(manufacturer['manufacturerName'], datatype=XSD.string)))
        
    g_state.serialize(destination=str(OUTPUT_PATH_STATE), format='turtle')
    g_city.serialize(destination=str(OUTPUT_PATH_CITY), format='turtle')
    g_airport.serialize(destination=str(OUTPUT_PATH_AIRPORT), format='turtle')
    g_carrier.serialize(destination=str(OUTPUT_PATH_CARRIER), format='turtle')
    g_aircraft.serialize(destination=str(OUTPUT_PATH_AIRCRAFT), format='turtle')
    g_model.serialize(destination=str(OUTPUT_PATH_MODEL), format='turtle')
    g_manufacturer.serialize(destination=str(OUTPUT_PATH_MANUFACTURER), format='turtle')
if __name__ == "__main__":
    serialize_to_ttl()
