import csv
import os

def convert_master_to_csv():
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

if __name__ == "__main__":
    convert_master_to_csv()
