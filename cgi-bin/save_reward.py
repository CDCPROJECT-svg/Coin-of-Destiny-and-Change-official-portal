#!/usr/bin/env python3
import cgi, cgitb, json, csv, os
cgitb.enable()

print("Content-Type: text/plain\n")

try:
    length = int(os.environ.get('CONTENT_LENGTH',0))
    data = json.loads(os.read(0,length))
    username = data.get('username')
    level = data.get('level')
    incentive = data.get('incentive', 'NONE')

    if not username or not level:
        print("Missing username or level!")
        exit()

    csv_file = '../codac_wallets.csv'
    with open(csv_file,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, f'Leadership Level {level}', incentive])

    msg = f"Success: {username} claimed Leadership Level {level} reward ({incentive}) and points reset to 0."
    if int(level) == 18:
        msg += " Graduation complete! Auto-enter Cycle 2 Feeding Area with 50% engagement."
    print(msg)

except Exception as e:
    print("Error:", e)
