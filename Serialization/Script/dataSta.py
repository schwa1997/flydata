from pathlib import Path
import pandas as pd
from tabulate import tabulate

BASE_PATH = Path(r"C:\Users\14369\Desktop\flydata")
STATE_PATH = BASE_PATH / "DataCollection" / "CSVData" / "states.csv"
CITIES_PATH = BASE_PATH / "DataCollection" / "CSVData" / "cities.csv"
AIRPORTS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "airports.csv"
CARRIERS_PATH = BASE_PATH / "DataCollection" / "CSVData" / "carriers.csv"
AIRCRAFT_PATH = BASE_PATH / "DataCollection" / "CSVData" / "aircrafts.csv"
MODEL_PATH = BASE_PATH / "DataCollection" / "CSVData" / "model.csv"
MANUFACTURER_PATH = BASE_PATH / "DataCollection" / "CSVData" / "manufacturer.csv"


def get_file_statistics():
    stats = []
    file_paths = {
        "States": STATE_PATH,
        "Cities": CITIES_PATH,
        "Airports": AIRPORTS_PATH,
        "Carriers": CARRIERS_PATH,
        "Aircraft": AIRCRAFT_PATH,
        "Models": MODEL_PATH,
        "Manufacturers": MANUFACTURER_PATH
    }
    
    print("\nChecking data files...")
    for name, path in file_paths.items():
        try:
            if not path.exists():
                print(f"Warning: File not found - {path}")
                stats.append([name, "N/A", "N/A", "N/A"])
                continue
                
            df = pd.read_csv(path)
            row_count = len(df)
            column_count = len(df.columns)
            column_names = ", ".join(df.columns)
            stats.append([
                name, 
                row_count,
                column_count,
                column_names
            ])
            print(f"✓ Successfully read {name} data")
        except Exception as e:
            print(f"Error reading {name} file: {str(e)}")
            stats.append([name, "Error", "Error", "Error"])
    
    if not stats:
        print("No data files found to process!")
        return
        
    # Display the table
    print("\nDetailed Dataset Statistics:")
    print(tabulate(stats, headers=["Dataset", "Rows", "Columns", "Column Names"], tablefmt="grid"))

if __name__ == "__main__":
    get_file_statistics()
