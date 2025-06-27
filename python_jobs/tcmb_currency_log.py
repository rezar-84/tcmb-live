import requests
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET
from openpyxl import Workbook

# Define the start and end dates
start_date = datetime(2017, 11, 20)
end_date = datetime.now()

# Create a new Excel workbook and worksheet
wb = Workbook()
ws = wb.active
ws.title = "Currency Rate"
ws.append(["Id", "Currency", "Rate", "Date", "Company"])

# Counter for ID
row_id = 1

# Fetch exchange rate for a given date
def fetch_tcmb_rate(date):
    try:
        url = f"https://www.tcmb.gov.tr/kurlar/{date.strftime('%Y%m')}/{date.strftime('%d%m%Y')}.xml"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ No data for {date.strftime('%Y-%m-%d')} (status code: {response.status_code})")
            return None

        tree = ET.fromstring(response.content)
        for currency in tree.findall("Currency"):
            if currency.attrib.get("Kod") == "EUR":
                rate = currency.find("ForexBuying").text
                return float(rate)
    except Exception as e:
        print(f"⚠️ Error fetching {date.strftime('%Y-%m-%d')}: {e}")
        return None

# Recursive loop to go through each day
def fetch_all_rates(current_date):
    global row_id
    if current_date > end_date:
        print("✅ All done!")
        wb.save("Currency_Rate_TCMB-log.xlsx")
        print("📁 Saved as Currency_Rate_TCMB-log.xlsx")
        return

    if current_date.weekday() < 5:  # Weekdays only
        print(f"📅 Processing {current_date.strftime('%Y-%m-%d')}...")
        rate = fetch_tcmb_rate(current_date)
        if rate:
            formatted_date = current_date.strftime("%Y-%m-%d 11:00:00")
            ws.append([row_id, "EUR", rate, formatted_date, "Your Company"])
            print(f"✅ Found rate: {rate}")
            row_id += 1
        else:
            print(f"⚠️ No rate found for {current_date.strftime('%Y-%m-%d')}")
    else:
        print(f"🛌 Skipping weekend: {current_date.strftime('%Y-%m-%d')}")

    # Recursive call for next day
    fetch_all_rates(current_date + timedelta(days=1))

# Start the loop
fetch_all_rates(start_date)

