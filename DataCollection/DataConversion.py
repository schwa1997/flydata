import pandas as pd
import unicodedata

def convert_excel_to_csv(excel_file, csv_file):
    df = pd.read_excel(excel_file)
    
    # Clean the data
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # For string columns, handle special characters
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].apply(lambda x: 
            unicodedata.normalize('NFKD', str(x)) if pd.notna(x) else x)
        
        # Replace problematic characters
        df[col] = df[col].apply(lambda x: 
            x.replace('"', '').replace("'", '') if pd.notna(x) else x)
    
    # Save with UTF-8 encoding and BOM
    df.to_csv(csv_file, index=False, encoding='utf-8', quoting=0)
    print(f'Converted {excel_file} to {csv_file}')

def convert_dat_to_csv(dat_file, csv_file, column_names):
    try:
        # Try reading with UTF-8 encoding
        df = pd.read_csv(dat_file, 
                        header=None, 
                        names=column_names,
                        encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, try reading with 'latin1' encoding
        df = pd.read_csv(dat_file, 
                        header=None, 
                        names=column_names,
                        encoding='latin1')
    
    # Clean the data
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # For string columns, handle special characters
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].apply(lambda x: 
            unicodedata.normalize('NFKD', str(x)) if pd.notna(x) else x)
        
        # Replace problematic characters
        df[col] = df[col].apply(lambda x: 
            x.replace('"', '').replace("'", '') if pd.notna(x) else x)
    
    # Save with UTF-8 encoding and BOM
    df.to_csv(csv_file, index=False, encoding='utf-8-sig', quoting=1)
    print(f'Converted {dat_file} to {csv_file}')

# File paths
BASE_PATH_ORIGINAL = r'C:\Users\14369\Desktop\flydata\DataCollection\OriginalData'
BASE_PATH_CSV = r'C:\Users\14369\Desktop\flydata\DataCollection\CSVData'

FILES = {
    'aircrafts': {
        'input': f'{BASE_PATH_ORIGINAL}/7-aircrafts.dat',
        'output': f'{BASE_PATH_CSV}/aircrafts.csv',
        'columns': ['Name', 'IATA code', 'ICAO code']
    },
    'airports': {
        'input': f'{BASE_PATH_ORIGINAL}/3-airport.dat',
        'output': f'{BASE_PATH_CSV}/airports.csv',
        'columns': ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 
                   'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 
                   'Tz database', 'Timezone Type', 'Source']
    },
    'carriers': {
        'input': f'{BASE_PATH_ORIGINAL}/6-carriers.dat',
        'output': f'{BASE_PATH_CSV}/carriers.csv',
        'columns': ['AirlineID', 'Name', 'Alias', 'IATA', 'ICAO', 'Callsign', 
                   'Country', 'Active']
    },
    'cities': {
        'input': f'{BASE_PATH_ORIGINAL}/2-cities.xlsx',
        'output': f'{BASE_PATH_CSV}/cities.csv'
    },
    'routes': {
        'input': f'{BASE_PATH_ORIGINAL}/4-routes.dat',
        'output': f'{BASE_PATH_CSV}/routes.csv',
        'columns': ['Airline', 'Airline ID', 'Source airport', 'Source airport ID',
                   'Destination airport', 'Destination airport ID', 'Codeshare', 
                   'stops', 'Equipment']
    },
  
}

def main():
    # Process Excel files
    for file_type in ['cities']:
        convert_excel_to_csv(
            FILES[file_type]['input'],
            FILES[file_type]['output']
        )

    # Process DAT files
    for file_type in ['aircrafts', 'airports', 'carriers', 'routes']:
        convert_dat_to_csv(
            FILES[file_type]['input'],
            FILES[file_type]['output'],
            FILES[file_type]['columns']
        )

if __name__ == "__main__":
    main()

