from odoo import models, fields
import requests
from lxml import etree
from datetime import datetime

class CurrencyProviderTCMB(models.Model):
    _name = "currency.provider.tcmb"
    _inherit = "currency.provider"
    _description = "TCMB Forex Buying Rates"

    def _get_rates(self, currencies):
        return self.get_rates_by_date(currencies, fields.Date.today())

    def get_rates_by_date(self, currencies, date):
        base_url = "https://www.tcmb.gov.tr/kurlar/"
        result = {}

        try:
            date_obj = fields.Date.from_string(date)
            yyyy = date_obj.strftime('%Y')
            mm = date_obj.strftime('%m')
            ddmmyyyy = date_obj.strftime('%d%m%Y')
            url = f"{base_url}{yyyy}{mm}/{ddmmyyyy}.xml"
            res = requests.get(url, timeout=10)
            tree = etree.fromstring(res.content)

            for currency in currencies:
                tc_code = currency.name
                node = tree.xpath(f"//Currency[@CurrencyCode='{tc_code}']/ForexBuying")
                if node and node[0].text:
                    try:
                        result[currency] = 1 / float(node[0].text.replace(',', '.'))
                    except Exception:
                        continue
        except Exception:
            pass

        return result

    def update_rates_for_date(self, date):
        Currency = self.env['res.currency']
        Rate = self.env['res.currency.rate']
        currencies = Currency.search([('name', '!=', 'TRY')])
        rates = self.get_rates_by_date(currencies, date)

        for currency, rate in rates.items():
            existing = Rate.search([
                ('currency_id', '=', currency.id),
                ('name', '=', date)
            ])
            if existing:
                existing.write({'rate': rate})
            else:
                Rate.create({
                    'currency_id': currency.id,
                    'name': date,
                    'rate': rate,
                })

    def manual_sync_tcmb_rates(self):
        today = fields.Date.today()
        self.update_rates_for_date(today)
