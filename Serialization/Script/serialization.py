import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace, XSD, RDFS, FOAF

# Define all paths
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
STATE_PATH = BASE_PATH / "DataCollection" / "CSVData" / "states.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CARRIERS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "carriers.csv"
AIRCRAFT_PATH = BASE_PATH / "DataCollection" / "CSVData" / "aircrafts.csv"
MODEL_PATH = BASE_PATH / "DataCollection" / "CSVData" / "model.csv"
MANUFACTURER_PATH = BASE_PATH / "DataCollection" / "CSVData" / "manufacturer.csv"
# Output paths
OUTPUT_PATH_AIRPORT = BASE_PATH / "Serialization" /"ttl"/ "airports.ttl"
OUTPUT_PATH_CARRIER = BASE_PATH / "Serialization" / "ttl" / "carriers.ttl"
OUTPUT_PATH_STATE = BASE_PATH / "Serialization" /"ttl"/ "states.ttl"
OUTPUT_PATH_CITY = BASE_PATH / "Serialization" /"ttl"/ "cities.ttl"
OUTPUT_PATH_AIRCRAFT = BASE_PATH / "Serialization" /"ttl"/ "aircrafts.ttl"
OUTPUT_PATH_MODEL = BASE_PATH / "Serialization" /"ttl"/ "models.ttl"
OUTPUT_PATH_MANUFACTURER = BASE_PATH / "Serialization" /"ttl"/ "manufacturers.ttl"

def read_cities():
    cities = {}
    try:
        with open(CITIES_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city_ascii = str(row['city_ascii'])
                if row['city_ascii'] and row['city'] and row['state_id']:
                    cities[city_ascii] = {
                        'name': row['city'].strip(),
                        'population': str(row['population']) if pd.notna(row['population']) else "0",
                        'state_id': str(row['state_id']) 
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
                if row['IATA']:  
                    carriers.append({
                        'name': row['Name'].strip('"'),
                        'iata': row['IATA'].strip('"'),
                        'callsign': row['Callsign'].strip('"'),
                        'airline_id': row['\ufeffAirlineID'].strip('"')  
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
                if row['IATA']: 
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
                    'model_code': row['ModelCode'].strip(),
                    'aircraft_type': row['AircraftType'].strip(),
                    'register_city': row['RegisterCity'].strip()
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
                    'model_name': row['ModelName'].strip(),
                    'manufacture_code': row['ModelCode'].strip()
                })
    except Exception as e:
        print(f"Error reading model file: {str(e)}")
        raise
    return model

def serialize_to_ttl():
    g_state = Graph()
    g_city = Graph()
    g_airport = Graph()
    g_carrier = Graph()
    g_aircraft = Graph()
    g_model = Graph()
    g_manufacturer = Graph()
    
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    for g in [g_state, g_city, g_airport, g_carrier, g_aircraft, g_model, g_manufacturer]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)

    states = read_states()
    print("states.csv read")
    cities = read_cities()
    print("cities.csv read")
    carriers = read_carriers()
    print("carriers.csv read")
    airports = read_airports()
    print("airports.csv read")
    aircrafts = read_aircrafts()
    print("aircrafts.csv read")
    models = read_model()
    print("models.csv read")
    manufacturers = read_manufacturer()
    print("manufacturers.csv read")
    
    model_uri_mapping = {model['model_code']: FDO[model['model_code']] for model in models}
    manufacturer_uri_mapping = {mfr['manufacture_code']: FDO[mfr['manufacture_code']] for mfr in manufacturers}
    state_uri_mapping = {state['abbreviation']: FDO[state['abbreviation']] for state in states}
    city_uri_mapping = {}
    for city_ascii, city_data in cities.items():
        city_name = city_data['name']
        city_id = quote(city_name.encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
        city_uri_mapping[city_name] = FDO[city_id]

    for city_ascii, city_data in cities.items():
        city_uri = city_uri_mapping[city_data['name']]
        g_city.add((city_uri, RDF.type, FDO.City))
        g_city.add((city_uri, FDO.name, Literal(city_data['name'], datatype=XSD.string)))
        g_city.add((city_uri, FDO.population, Literal(city_data['population'], datatype=XSD.string)))
       
        if city_data['state_id'] in state_uri_mapping:
            state_uri = state_uri_mapping[city_data['state_id']]
            g_city.add((city_uri, FDO.isLocatedInState, state_uri))
    print("cities.ttl created")

    for state in states:
        state_uri = state_uri_mapping[state['abbreviation']]
        g_state.add((state_uri, RDF.type, FDO.State))
        g_state.add((state_uri, FDO.abbreviation, Literal(state['abbreviation'], datatype=XSD.string)))
        g_state.add((state_uri, FDO.name, Literal(state['name'], datatype=XSD.string)))
    print("states.ttl created")
    for airport in airports:
        airport_uri = URIRef(str(FDO) + airport['iata'])
        g_airport.add((airport_uri, RDF.type, FDO.Airport))
        g_airport.add((airport_uri, FDO.name, Literal(airport['name'], datatype=XSD.string)))
        if airport['city'] in cities:
            city_id = quote(airport['city'].encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
            city_uri = URIRef(str(FDO) + city_id)
            g_airport.add((airport_uri, FDO.isLocatedInCity, city_uri))
    print("airports.ttl created")
    for carrier in carriers:
        carrier_uri = FDO[carrier['iata']]
        g_carrier.add((carrier_uri, RDF.type, FDO.Carrier))
        g_carrier.add((carrier_uri, FDO.name, Literal(carrier['name'], datatype=XSD.string)))
        g_carrier.add((carrier_uri, FDO.callSign, Literal(carrier['callsign'], datatype=XSD.string)))
    print("carriers.ttl created")
    # Create model URI mapping before the aircraft loop

    for aircraft in aircrafts:
        encoded_n_number = quote(aircraft['n_number'].strip())
        aircraft_uri = FDO[encoded_n_number]
        g_aircraft.add((aircraft_uri, RDF.type, FDO.Aircraft))
        g_aircraft.add((aircraft_uri, FDO.aircraftType, Literal(aircraft['aircraft_type'], datatype=XSD.string)))

        if aircraft['model_code']:
            model_code = aircraft['model_code']
            model_uri = model_uri_mapping[model_code]
            g_aircraft.add((aircraft_uri, FDO.hasModel, model_uri))
    print("aircrafts.ttl created")
 
    for model in models:
        model_uri = model_uri_mapping[model['model_code']]
        g_model.add((model_uri, RDF.type, FDO.Model))
        g_model.add((model_uri, FDO.name, Literal(model['model_name'], datatype=XSD.string)))
        g_model.add((model_uri, FDO.modelCode, Literal(model['model_code'], datatype=XSD.string)))
        
        if model['manufacture_code'] in manufacturer_uri_mapping:
            manufacturer_uri = manufacturer_uri_mapping[model['manufacture_code']]
            g_model.add((model_uri, FDO.hasManufacturer, manufacturer_uri))
    print("models.ttl created")
    for manufacturer in manufacturers:
        manufacturer_uri = URIRef(str(FDO) + manufacturer['manufacture_code'])
        g_manufacturer.add((manufacturer_uri, RDF.type, FDO.Manufacturer))
        g_manufacturer.add((manufacturer_uri, FDO.name, Literal(manufacturer['manufacturer_name'], datatype=XSD.string)))
    print("manufacturers.ttl created")
    g_state.serialize(destination=str(OUTPUT_PATH_STATE), format='turtle')
    print("states.ttl serialized")
    g_city.serialize(destination=str(OUTPUT_PATH_CITY), format='turtle')
    print("cities.ttl serialized")
    g_airport.serialize(destination=str(OUTPUT_PATH_AIRPORT), format='turtle')
    print("airports.ttl serialized")
    g_carrier.serialize(destination=str(OUTPUT_PATH_CARRIER), format='turtle')
    print("carriers.ttl serialized")
    g_aircraft.serialize(destination=str(OUTPUT_PATH_AIRCRAFT), format='turtle')
    print("aircrafts.ttl serialized")
    g_model.serialize(destination=str(OUTPUT_PATH_MODEL), format='turtle')
    print("models.ttl serialized")
    g_manufacturer.serialize(destination=str(OUTPUT_PATH_MANUFACTURER), format='turtle')
    print("manufacturers.ttl serialized")
if __name__ == "__main__":
    serialize_to_ttl()