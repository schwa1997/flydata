import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

# Define all paths
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")

ROUTES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "routes.csv"
CARRIERS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "carriers.csv"
OUTPUT_PATH_CARRIER = BASE_PATH / "Serialization" / "ttl" / "carrier.ttl"

def read_routes():
    routes = []
    try:
        with open(ROUTES_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Print column names to debug
            print("Available columns:", reader.fieldnames)
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

def read_carriers():
    carriers = []
    try:
        with open(CARRIERS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Print column names to debug
            print("Carrier columns:", reader.fieldnames)
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

def serialize_to_ttl():
    # Create a new RDF graph
    g = Graph()
    
    # Define namespaces with your ontology URL
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    g.bind("fdo", FDO)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    
    # Read data
    carriers = read_carriers()
    routes = read_routes()
    
    # Create carrier nodes and their routes
    for carrier in carriers:
        carrier_uri = FDO[carrier['iata']]
        g.add((carrier_uri, RDF.type, FDO.Carrier))
        g.add((carrier_uri, RDFS.label, Literal(carrier['name'])))
        g.add((carrier_uri, FDO.callSign, Literal(carrier['callsign'])))
        # Add routes for this carrier
        for route in routes:
            if route['airline'] == carrier['iata']:
                route_uri = FDO[f"{route['source_airport']}{route['destination_airport']}"]
                g.add((carrier_uri, FDO.hasRoute, route_uri))

    # Serialize to TTL file
    g.serialize(destination=str(OUTPUT_PATH_CARRIER), format="turtle")
    print(f"Carrier TTL file created at: {OUTPUT_PATH_CARRIER}")

if __name__ == "__main__":
    serialize_to_ttl()
