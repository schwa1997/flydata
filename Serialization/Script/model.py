import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

# Define all paths
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
MODEL_PATH = BASE_PATH / "DataCollection" / "CSVData" / "model.csv"
MANUFACTURER_PATH = BASE_PATH / "DataCollection" / "CSVData" / "manufacturer.csv"
AIRCRAFT_PATH = BASE_PATH / "DataCollection" / "CSVData" / "aircrafts.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
# Output paths
OUTPUT_PATH_MODEL = BASE_PATH / "Serialization" /"ttl"/ "model.ttl"
OUTPUT_PATH_MANUFACTURER = BASE_PATH / "Serialization" /"ttl"/ "manufacturer.ttl"
OUTPUT_PATH_AIRCRAFT = BASE_PATH / "Serialization" /"ttl"/ "aircrafts.ttl"

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
def serialize_to_ttl():
    # Create RDF graphs
    g_model = Graph()
    g_manufacturer = Graph()
    g_aircraft = Graph()
    
    # Define namespaces
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    
    # Bind namespaces for all graphs
    for g in [g_model, g_manufacturer, g_aircraft]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)
    

    # Load all data
    model = read_model()
    manufacturer = read_manufacturer()
    aircrafts = read_aircrafts()
    cities = read_cities()

    # Create model mappings andadd model data first
    model_uri_mapping = {}
    for model_data in model:
        model_uri_mapping[model_data['model_code']] = URIRef(str(FDO) + quote(model_data['model_code']))

    # Create manufacturer mappings first
    manufacturer_uri_mapping = {}
    for mfr in manufacturer:
        manufacturer_uri_mapping[mfr['manufacture_code']] = URIRef(str(FDO) + quote(mfr['manufacture_code']))

    for model_data in model:
        model_uri = model_uri_mapping[model_data['model_code']]
        g_model.add((model_uri, RDF.type, FDO.Model))
        g_model.add((model_uri, FDO.name, Literal(model_data['model_name'], datatype=XSD.string)))
        g_model.add((model_uri, FDO.modelCode, Literal(model_data['model_code'], datatype=XSD.string)))
        g_model.add((model_uri, FDO.hasManufacturer, manufacturer_uri_mapping[model_data['model_code']]))
   
    for mfr_data in manufacturer:
        manufacturer_uri = manufacturer_uri_mapping[mfr_data['manufacture_code']]
        g_manufacturer.add((manufacturer_uri, RDF.type, FDO.Manufacturer))
        g_manufacturer.add((manufacturer_uri, FDO.name, Literal(mfr_data['manufacturer_name'], datatype=XSD.string)))

    for aircraft in aircrafts:
        # Properly encode the N-number for the URI
        encoded_n_number = quote(aircraft['n_number'].strip())
        aircraft_uri = FDO[encoded_n_number]
        g_aircraft.add((aircraft_uri, RDF.type, FDO.Aircraft))
        # g_aircraft.add((aircraft_uri, FDO.name, Literal(aircraft['n_number'], datatype=XSD.string)))
        g_aircraft.add((aircraft_uri, FDO.aircraftType, Literal(aircraft['aircraft_type'], datatype=XSD.integer)))
        g_aircraft.add((aircraft_uri, FDO.isRegisteredInCity, Literal(aircraft['register_city'], datatype=XSD.string)))
        
        if aircraft['register_city'] in cities:
            city_id = quote(aircraft['register_city'].encode('ascii', 'ignore').decode().replace(" ", "_").replace("'", "").replace(",", ""))
            city_uri = URIRef(str(FDO) + city_id)
            g_aircraft.add((aircraft_uri, FDO.isRegisteredInCity, city_uri))
        if aircraft['model_code']:
            model_code = aircraft['model_code']
            model_uri = model_uri_mapping[model_code]
            g_aircraft.add((aircraft_uri, FDO.hasModel, model_uri))
  
    g_aircraft.serialize(destination=str(OUTPUT_PATH_AIRCRAFT), format='turtle')
    g_model.serialize(destination=str(OUTPUT_PATH_MODEL), format='turtle')
    g_manufacturer.serialize(destination=str(OUTPUT_PATH_MANUFACTURER), format='turtle')
if __name__ == "__main__":
    serialize_to_ttl()
