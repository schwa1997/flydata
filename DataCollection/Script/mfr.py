import pandas as pd
import unicodedata
import os
import csv
def convert_mfr_to_csv():
    # Input and output file paths
    BASE_PATH_ORIGINAL = r'C:\Users\huimin.chen\projects\chm-graphdb\flydata\DataCollection\OriginalData'
    BASE_PATH_CSV = r'C:\Users\huimin.chen\projects\chm-graphdb\flydata\DataCollection\CSVData'
    
    input_file = f'{BASE_PATH_ORIGINAL}/MFR.txt'
    output_file = f'{BASE_PATH_CSV}/mfr.csv'
    
    try:
        with open(input_file, 'r') as txt_file:
            lines = txt_file.readlines()
            
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write header for selected columns
                writer.writerow(['mfrCode', 'manufaturerName','modelName'])
                
                # Process each line, skip the first line
                for i, line in enumerate(lines):
                    if i == 0:  # Skip the first line
                        continue
                        
                    mfrCode = line[0:7].strip()
                    manufaturerName = line[8:38].strip()
                    modelName = line[39:59].strip()

                    writer.writerow([mfrCode, manufaturerName,modelName])
                    
        print(f"Successfully converted {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    convert_mfr_to_csv()