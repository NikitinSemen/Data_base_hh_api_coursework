from pprint import pprint

import requests
from typing import Any
import psycopg2


def get_data_from_hh(employer_id: list) -> list[dict[str:Any]]:
    """Функция для получение данных о компаниях и вакансиях этих компаний с HeadHunter"""
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
    for item in range(len(items)):
        company = items[item]['employer']
        vacancy = {'name': items[item]['name'],
                   'published_at': items[item]['published_at'],
                   'requirement': items[item]['snippet'],
                   'salary': items[item]['salary'],
                   'experience': items[item]['experience']['name']
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
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(100),
                url TEXT
                )
        ''')
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE ads (
                ads_id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES company(company_id),
                ads_name VARCHAR(255),
                data_published DATE,
                requirement TEXT,
                responsibility TEXT,
                salary_from INTEGER,
                experience VARCHAR(255)
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
            cur.execute(f'''INSERT INTO company(company_name, url) VALUES (%s, %s) RETURNING company_id ''',
                        (item['company']['name'].split(',')[0], item['company']['alternate_url']))
            company_id = cur.fetchone()[0]

            cur.execute(
                '''
                INSERT INTO ads (
                company_id,
                ads_name, 
                data_published,
                requirement,
                responsibility)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (company_id, item['vacancy']['name'],
                 item['vacancy']['published_at'],
                 item['vacancy']['requirement']['requirement'],
                 item['vacancy']['requirement']['responsibility'])
            )

    conn.commit()
    conn.commit()
    conn.close()

# kaka = get_data_from_hh('1942330')
# pprint(kaka)
