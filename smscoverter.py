import xml.etree.ElementTree as ET
import csv
from datetime import datetime

input_file='static\sample_sms_backup.xml'
output_file='message.csv'

tree=ET.parse(input_file)
root=tree.getroot()

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "address", "message"])

    for sms in root.findall("sms"):
        address = sms.get("address", "")
        body = sms.get("body", "")
        date_ms = sms.get("date", "")

        # convert ms timestamp to readable time (optional)
        try:
            dt = datetime.fromtimestamp(int(date_ms) / 1000)
            date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            date_str = ""

        writer.writerow([date_str, address, body])

print("Saved basic messages to", output_file)