import random
import time
from datetime import datetime

OUTPUT = "static/sample_sms_backup.xml"

def random_date_ms():
    return int(time.time() * 1000) - random.randint(0, 3000000000)

fake_banks = ["ICICIBNK", "HDFCBNK", "KOTAKBNK", "INDBNK", "SBI", "PNB", "AXISBNK"]
fake_persons = ["RAHUL", "BALAJI", "ANITA", "MOHIT", "NEHA", "PRAVEEN", "ARJUN"]
fake_merchant = ["ZOMATO", "SWIGGY", "AMAZON", "FLIPKART", "TATACLIQ", "NETFLIX", "SPOTIFY"]
fake_upi = ["ybl", "axl", "ibl", "okicici", "oksbi", "okaxis"]

def make_sms(i):
    date = random_date_ms()
    readable = datetime.fromtimestamp(date / 1000).strftime("%b %d, %Y %I:%M:%S %p")
    bank = random.choice(fake_banks)
    amt = random.randint(10, 20000)
    person = random.choice(fake_persons)
    merch = random.choice(fake_merchant)
    upi = random.choice(fake_upi)

    body_options = [
        f"A/c *9745 debited Rs. {amt}.00 to {person} via UPI:{random.randint(100000,999999)}.{upi}",
        f"A/c *9745 credited Rs. {amt}.00 from {person}. UPI REF:{random.randint(1000000,9999999)}",
        f"Payment of Rs.{amt}.00 to {merch} successful. UPI ID: 9845{random.randint(1000,9999)}.{upi}",
        f"Rs.{amt} received from {person}. Check your passbook for balance update.",
        f"IMPORTANT: Do not share OTP, UPI PIN, or CVV with anyone.",
        f"Recharge successful Rs.{amt}, enjoy data benefits.",
    ]
    body = random.choice(body_options)

    return f'''  <sms protocol="0" address="AX-{bank}-S" date="{date}" type="1" body="{body}" readable_date="{readable}" contact_name="(Unknown)" />'''

# ============================
# WRITE XML
# ============================

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n")
    f.write(f"<smses count=\"300\" backup_set=\"SAMPLE-DEMO-DATA\" backup_date=\"{int(time.time()*1000)}\" type=\"full\">\n")

    for i in range(300):
        f.write(make_sms(i) + "\n")

    f.write("</smses>")

print(f"Saved sample 300 SMS XML to {OUTPUT}")
