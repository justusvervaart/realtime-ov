import requests
import csv
import datetime
from dateutil import parser
import pytz

def fetch_data_and_write_to_csv():
    # API URL
    url = "https://www.schiphol.nl/api/proxy/v3/waittimes/security-filters"
    
    # Send GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get data in JSON format
        data = response.json()

        # File name is static now
        filename = 'schiphol-security-scrape.csv'

        # Open the file in append mode
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            
            # Write header if file is empty
            if f.tell() == 0:
                writer.writerow(['Location', 'Updated', 'WaitTimeInSeconds'])

            # Iterate over each record
            for key, item in data.items():
                # Convert 'updated' to datetime object
                updated_time = parser.parse(item['updated'])
                # Convert to GMT+2
                updated_time = updated_time.astimezone(pytz.timezone('Etc/GMT-2'))
                # Convert back to string, without microseconds
                updated_time_str = updated_time.strftime('%Y-%m-%dT%H:%M:%S')
                # Write record to CSV
                writer.writerow([key, updated_time_str, item['waitTimeInSeconds']])
    else:
        print(f'GET request failed with status code: {response.status_code}')

# Call the function
fetch_data_and_write_to_csv()
