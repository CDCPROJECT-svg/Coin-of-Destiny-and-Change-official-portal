#!/usr/bin/env python3

import cgi
import cgitb
import json
import csv
import os

cgitb.enable()

# Set headers for CGI
print("Content-Type: text/plain\n")

try:
    # Read POST JSON data
    length = int(os.environ.get('CONTENT_LENGTH', 0))
    data = json.loads(os.read(0, length))
    
    username = data.get('username')
    level = data.get('level')
    incentive = data.get('incentive')

    if not all([username, level, incentive]):
        print("Missing data!")
        exit()

    csv_file = '../codac_wallets.csv'  # Path relative to CGI script

    # Append to CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, f'Leadership Level {level}', incentive])

    print(f'Success: {username} selected {incentive} for Leadership Level {level}')

except Exception as e:
    print("Error:", e)
