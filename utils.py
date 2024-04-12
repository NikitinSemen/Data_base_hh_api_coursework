import requests
import json
from pprint import pprint


def get_data_from_hh(employer_id):
    params = {
        "per_page": 20,
        "employer_id": employer_id,
        "only_with_salary": True,
        "area": 1,
        "only_with_vacancies": True
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    items = response.json()['items']
    data = []
    for item in items:
        if item['address']:
            vacancy = {'company_name': item.get('employer').get('name'),
                       'company_address': item.get('address').get('raw'),
                       'ad_name': item.get('name'),
                       'requirement': item.get("snippet").get('requirement'),
                       'responsibility': item.get("snippet").get('responsibility'),
                       'experience': item.get('experience').get('name')
                       }
            data.append(vacancy)
    return data


