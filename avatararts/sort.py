import csv

# Define the input and output file paths
input_csv = '/Users/steven/Pictures/DaLL-E/dalle.csv'
output_csv = '/Users/steven/Pictures/DaLL-E/sorted_dalle.csv'

# Function to parse the input CSV and extract URL and INFO
def parse_csv(input_path):
    with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # Skip the header row if there is one

        # Collect the data from the input file
        data = []
        for row in reader:
            # Concatenate the URL and INFO if they are split into different rows
            row_data = ' '.join(row)
            parts = row_data.split('https://')
            for part in parts:
                if part.strip():
                    url = 'https://' + part.split()[0]
                    info = ' '.join(part.split()[1:])
                    data.append([url, info])
    return data

# Sort the data based on the URL
def sort_data(data):
    return sorted(data, key=lambda x: x[0])

# Write the sorted data to the output CSV file
def write_csv(data, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['URL', 'INFO'])  # Write the header row
        writer.writerows(data)

# Main function to process the CSV
def main():
    data = parse_csv(input_csv)
    sorted_data = sort_data(data)
    write_csv(sorted_data, output_csv)
    print(f"Data sorted and saved to {output_csv}")

if __name__ == "__main__":
    main()
