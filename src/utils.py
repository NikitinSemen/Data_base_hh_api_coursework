import requests
from typing import Any
import psycopg2


def get_data_from_hh(employer_id: list) -> list[dict[str:Any]]:
    """Функция для получение данных о компаниях и вакансиях этих компаний с HeadHunter"""
    data = []
    for i in employer_id:
        params = {
            "per_page": 20,
            "employer_id": i,
            "only_with_salary": True,
            "area": 1,
            "only_with_vacancies": True
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        items = response.json()['items']

        for item in range(len(items)):
            company = items[item]['employer']
            vacancy = {'company_id': items[item]['employer']['id'],
                       'name': items[item]['name'],
                       'salary': items[item]['salary'],
                       'url': items[item]['alternate_url']
                       }
            data.append({'company': company,
                         "vacancy": vacancy})

    return data


def create_data_base(name_database: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях с HeadHunter"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {name_database}')
    cur.execute(f'CREATE DATABASE {name_database}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=name_database, **params)
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE company (
                company_id int PRIMARY KEY,
                company_name VARCHAR(100)
                )
        ''')
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE ads (
                ads_id SERIAL PRIMARY KEY,
                company_id INTEGER NOT NULL,
                ads_name VARCHAR(255),
                salary_from INTEGER DEFAULT NULL,
                salary_to INTEGER DEFAULT NULL,
                url TEXT,
                FOREIGN KEY (company_id) REFERENCES company(company_id)
                )
        ''')
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str: Any]],
                          name_database: str, params: dict) -> None:
    """Сохраняет данные о вакансиях и компаниях в базу данных"""
    conn = psycopg2.connect(dbname=name_database, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                f'''INSERT INTO company (company_id, company_name)
                 VALUES (%s, %s)
                 ON CONFLICT (company_id) DO NOTHING ''',
                (item['company']['id'], item['company']['name'].split(',')[0]))

            cur.execute(
                '''
                INSERT INTO ads (
                company_id,
                ads_name, 
                salary_from,
                salary_to,
                url)
                VALUES (%s, %s, %s, %s, %s)
                
                ''',
                (item['vacancy']['company_id'],
                 item['vacancy']['name'],
                 item['vacancy']['salary']['from'],
                 item['vacancy']['salary']['to'],
                 item['vacancy']['url'])
            )

    conn.commit()
    conn.close()

