
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

# Function to fetch exchange rate from TCMB for a given date
def fetch_tcmb_rate(date):
    try:
        url = f"https://www.tcmb.gov.tr/kurlar/{date.strftime('%Y%m')}/{date.strftime('%d%m%Y')}.xml"
        response = requests.get(url)
        if response.status_code != 200:
            return None

        tree = ET.fromstring(response.content)
        for currency in tree.findall("Currency"):
            if currency.attrib.get("Kod") == "EUR":
                rate = currency.find("ForexBuying").text
                return float(rate)
    except Exception:
        return None

# Loop over each day in the date range
current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:  # Only weekdays
        rate = fetch_tcmb_rate(current_date)
        if rate:
            date_with_time = current_date.strftime("%Y-%m-%d 11:00:00")
            ws.append([row_id, "EUR", rate, date_with_time, "Your Company"])
            row_id += 1
    current_date += timedelta(days=1)

# Save the workbook
wb.save("Currency_Rate_TCMB.xlsx")
print("✅ Done! File saved as 'Currency_Rate_TCMB.xlsx'")
