from pprint import pprint
from utils import save_data_to_database, company, ads
from utils import create_data_base
from config import config
from utils import get_data_from_hh
import json

id_company_hh = [
    '1942330',  # Пятерочка
    '49357',  # Магнит розничная сеть
    '78638',  # Тинькофф
    '907268',  # Софт медиа групп
    '52389',  # ЦУМ
    '668259',  # Эскорт Сервис
    '1373',  # Аэрофлот
    '1834129',  # White Rabbit Family
    '2120',  # Азбука вкуса
    '87021',  # WILDBERRIES

]
params = config()
data_from_hh = get_data_from_hh(id_company_hh)
inf_company = company(data_from_hh)
company_inf = list(inf_company)
inf_ads = ads(data_from_hh)
# create_data_base('headhunter', params)
# save_data_to_database(inf_ads, company_inf, 'headhunter', params)
#
#
# # pprint(data_from_hh)
for i in company_inf:
    print(i)
