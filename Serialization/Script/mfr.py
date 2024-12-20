import pandas as pd
import csv
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, URIRef, Namespace, XSD, RDFS, FOAF

# Define all paths
BASE_PATH = Path(r"C:\Users\huimin.chen\projects\chm-graphdb\flydata")
mfr_path = BASE_PATH / "DataCollection" / "CSVData" / "mfr.csv"
# Output paths
output_path = BASE_PATH / "Serialization" /"ttl"/ "mfr.ttl"

def read_mfr():
    mfr = {}
    try:
        with open(mfr_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                mfr[row['mfrCode']] = { 
                    'manufacturerName': row['manufaturerName'],
                    'modelName': row['modelName']
                }
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        raise
    return mfr

def serialize_to_ttl():
    g_mfr = Graph()
    
    FDO = Namespace("http://www.semanticweb.org/nele/ontologies/2024/10/flydata/")
    for g in [g_mfr]:
        g.bind("fdo", FDO)
        g.bind("xsd", XSD)

    mfrs = read_mfr()
    print("mfr.csv read")
    
    # Add some debug prints
    print("First few items in mfrs:")
    for i, (code, data) in enumerate(list(mfrs.items())[:3]):
        print(f"  {i+1}. code: '{code}' ({type(code)})")
        print(f"     data: {data}")
    
    for mfr_code, mfr_data in mfrs.items():
        try:
            # Convert mfr_code to string explicitly (though it should already be one)
            mfr_code_str = str(mfr_code)
            mfr_uri = FDO[mfr_code_str]
            g_mfr.add((mfr_uri, RDF.type, FDO.Manufacturer))
            g_mfr.add((mfr_uri, FDO.name, Literal(mfr_data['manufacturerName'], datatype=XSD.string)))
            g_mfr.add((mfr_uri, FDO.modelName, Literal(mfr_data['modelName'], datatype=XSD.string)))
        except Exception as e:
            print(f"Error serializing mfr {mfr_code}: {str(e)}")
    print("mfr.ttl created")

    g_mfr.serialize(destination=str(output_path), format='turtle')
    print("mfr.ttl serialized")
if __name__ == "__main__":
    serialize_to_ttl()