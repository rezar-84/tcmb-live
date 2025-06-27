# 🇹🇷 TCMB Forex Buying Integration for Odoo + Python Excel Export

This repository provides a dual-purpose solution for integrating **TCMB (Central Bank of Turkey)** currency rates into your workflow:

1. `currency_provider_tcmb`: An Odoo 18 module to fetch **ForexBuying** rates with manual sync and historical support.
2. `export_tcmb_rates.py`: A standalone Python script to **fetch TCMB currency rates and export to Excel or CSV**.

---

## 📦 Odoo Module: `currency_provider_tcmb`

### ✅ Features

- Adds **TCMB** as a currency rate provider to Odoo.
- Uses **ForexBuying** rates from `https://www.tcmb.gov.tr/kurlar/`.
- Supports **manual sync** via UI button.
- Can fetch **historical rates** by specific date.
- Overrides Odoo's built-in rate providers when selected.

### 🛠 Installation

1. Clone this repository.
2. Copy the `currency_provider_tcmb/` directory into your Odoo `addons/` path.
3. Restart Odoo server.
4. In Odoo:
   - Activate **Developer Mode**
   - Go to **Apps > Update Apps List**
   - Search for and install **TCMB Forex Buying Currency Provider**
5. Navigate to **Accounting > Configuration > Currency Providers**
6. Select **TCMB Forex Buying**
7. Use the **Sync TCMB Rates** button to manually fetch today's rates.

---

## 🐍 Python Script: `export_tcmb_rates.py`

This script lets you fetch **TCMB ForexBuying** or other exchange rates by date and export them to `.xlsx` or `.csv`.

### ⚙️ Requirements

```bash
pip install requests pandas openpyxl
