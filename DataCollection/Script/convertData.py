import pandas as pd
import unicodedata
import os
import csv

# Constants
BASE_PATH_ORIGINAL = r'C:\Users\14369\Desktop\flydata\DataCollection\OriginalData'
BASE_PATH_CSV = r'C:\Users\14369\Desktop\flydata\DataCollection\CSVData'

FILES = {
    'aircrafts': {
        'input': f'{BASE_PATH_ORIGINAL}/7-aircrafts.dat',
        'output': f'{BASE_PATH_CSV}/aircrafts.csv',
        'columns': ['Name', 'IATA code', 'ICAO code']
    },
    # ... rest of FILES dictionary ...
}

# Helper functions
def clean_dataframe(df):
    """Clean and normalize dataframe contents."""
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].apply(lambda x: 
            unicodedata.normalize('NFKD', str(x)) if pd.notna(x) else x)
        
        # Replace problematic characters
        df[col] = df[col].apply(lambda x: 
            x.replace('"', '').replace("'", '') if pd.notna(x) else x)
    
    return df

def convert_aircraft_to_csv():
    BASE_PATH_ORIGINAL = r'C:\Users\14369\Desktop\flydata\DataCollection\OriginalData'
    BASE_PATH_CSV = r'C:\Users\14369\Desktop\flydata\DataCollection\CSVData'

    input_file = f'{BASE_PATH_ORIGINAL}/MASTER.txt'
    output_file = f'{BASE_PATH_CSV}/aircrafts.csv'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write header for selected columns
                writer.writerow(['AircraftID', 'ModelCode'])
                
                # Process each line
                for i, line in enumerate(lines):
                    if i == 0:  # Skip the first line
                        continue
                    n_number = line[0:5].strip()
                    model_code = line[37:44].strip()
    
                    
                    # Remove the commas from the extracted fields
                    n_number = 'N' + n_number
                    writer.writerow([n_number, model_code])
                    
        print(f"Successfully converted {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def convert_model_to_csv():
    # Input and output file paths
    BASE_PATH_ORIGINAL = r'C:\Users\14369\Desktop\flydata\DataCollection\OriginalData'
    BASE_PATH_CSV = r'C:\Users\14369\Desktop\flydata\DataCollection\CSVData'

    input_file = f'{BASE_PATH_ORIGINAL}/ACFTREF.txt'
    output_file = f'{BASE_PATH_CSV}/model.csv'
    
    try:
        with open(input_file, 'r') as txt_file:
            lines = txt_file.readlines()
            
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write header for selected columns
                writer.writerow(['ModelCode', 'ModelName'])
                
                # Process each line, skip the first line
                for i, line in enumerate(lines):
                    if i == 0:  # Skip the first line
                        continue
                        
                    modelCode = line[0:7].strip()
                    modelName = line[39:59].strip()
                    writer.writerow([modelCode, modelName])
                    
        print(f"Successfully converted {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    convert_master_to_csv()

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

