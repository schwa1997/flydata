import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

# Define all paths
BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
OUTPUT_PATH_AIRPORT = BASE_PATH / "Serialization" /"ttl"/ "airport.ttl"
OUTPUT_PATH_CITY = BASE_PATH / "Serialization" /"ttl"/ "city.ttl"

def read_cities():
    try:
        # Load the CSV file in memory using pandas
        cities_df = pd.read_csv(CITIES_PATH)
        cities = {}
        for _, row in cities_df.iterrows():
            # Convert city_ascii to string and skip if it's NaN
            if pd.isna(row['city_ascii']):
                continue
                
            city_ascii = str(row['city_ascii'])
            cities[city_ascii] = {
                'name': row['city'],
                'population': str(row['population']) if pd.notna(row['population']) else "0"
            }
                    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        raise

    return cities

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

def serialize_to_ttl():
    # Create two new RDF graphs
    g_airport = Graph()
    g_city = Graph()
    
    # Define namespaces
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    
    # Bind namespaces for both graphs
    for g in [g_airport, g_city]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)
    
    # Define the isLocatedInCity property in the airport graph
    g_airport.add((FDO.isLocatedInCity, RDF.type, RDF.Property))
    g_airport.add((FDO.isLocatedInCity, RDFS.domain, FDO.Airport))
    g_airport.add((FDO.isLocatedInCity, RDFS.range, FDO.City))
    
    cities = read_cities()
    airports = read_airports()
    
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

if __name__ == "__main__":
    serialize_to_ttl()
