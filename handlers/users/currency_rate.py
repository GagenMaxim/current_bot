import asyncio
import datetime
import requests
import xmltodict
from collections import namedtuple

Rate = namedtuple('Rate','name, rate')

def str_to_float(item:str):
    item = item.replace(',', '.')
    return float(item)

def get_rates():
    # URL запроса
    get_curl = "https://www.cbr.ru/scripts/XML_daily.asp"
    # Формат даты: день/месяц/год
    date_format = "%d/%m/%Y"
    # Дата запроса
    today = datetime.datetime.today()
    params ={
        "date_req": today.strftime(date_format),
    }
    r = requests.get(get_curl, params=params)
    resp = r.text

    data = xmltodict.parse(resp)
    # Ищем по @ID
    section_id = 'R01235'

    for item in data['ValCurs']['Valute']:
        if item['@ID'] == section_id:
            r = Rate(
                name = item['CharCode'],
                rate = str_to_float(item['Value']),
            )
            # print(r)
            return r
    return None

# # asyncio.run(get_rates())
# rate: object = asyncio.run(get_rates())

rate = get_rates()
# print(rate.rate)