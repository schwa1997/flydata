import csv
import os

def convert_master_to_csv():
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
