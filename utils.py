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
    for item in items:

        vacancy = {'company_name': item.get('employer').get('name'),
                   'company_address': item.get('area').get('name'),
                   'ad_name': item.get('name'),
                   'requirement': item.get("snippet").get('requirement'),
                   'responsibility': item.get("snippet").get('responsibility'),
                   'experience': item.get('experience').get('name'),
                   'published_at': item.get('published_at'),
                   'salary': item.get('salary')
                   }
        data.append(vacancy)
    return data
    # return items


def company(data):
    data_list = []
    for item in data:
        items = [item.get('company_name')]
        data_list.extend(items)

    return set(data_list)


def ads(data):
    ads_data = []
    for item in data:
        items = {'ad_name': item.get('ad_name'),
                 'requirement': item.get('requirement'),
                 'responsibility': item.get('responsibility'),
                 'experience': item.get('experience'),
                 "published_at": item.get('published_at')}
        ads_data.append(items)
    return ads_data


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
                address VARCHAR(255)
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


def save_data_to_database(data: list[dict[str: Any]], company_list: list, name_database: str, params: dict) -> None:
    """Сохраняет данные о вакансиях и компаниях в базу данных"""
    conn = psycopg2.connect(dbname=name_database, **params)
    with conn.cursor() as cur:
        for item in company_list:
            cur.execute(
                '''
                INSERT INTO company (company_name)
                VALUES (%s)
                RETURNING company_id
                ''',
                (item)
            )
            company_id = cur.fetchone()[0]
        for item in data:
            cur.execute(
                '''
                INSERT INTO ads (
                company_id
                ads_name, 
                data_published,
                requirement,
                responsibility)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (company_id, ['ad_name'], item['published_at'], item['requirement'], item['responsibility'])
            )

    conn.commit()
    conn.close()

# kaka = get_data_from_hh('1942330')
# pprint(kaka)
