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
# Output paths
OUTPUT_PATH_MODEL = BASE_PATH / "Serialization" /"ttl"/ "model.ttl"
OUTPUT_PATH_MANUFACTURER = BASE_PATH / "Serialization" /"ttl"/ "manufacturer.ttl"


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
def serialize_to_ttl():
    # Create RDF graphs
    g_model = Graph()
    g_manufacturer = Graph()
    
    # Define namespaces
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    
    # Bind namespaces for all graphs
    for g in [g_model, g_manufacturer]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)
    

    model = read_model()
    manufacturer = read_manufacturer()


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
        
    g_model.serialize(destination=str(OUTPUT_PATH_MODEL), format='turtle')
    g_manufacturer.serialize(destination=str(OUTPUT_PATH_MANUFACTURER), format='turtle')
if __name__ == "__main__":
    serialize_to_ttl()
