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
        if item['address']:
            vacancy = {'company_name': item.get('employer').get('name'),
                       'company_address': item.get('address').get('raw'),
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


def save_data_to_database(data: list[dict[str: Any]], name_database: str, params: dict) -> None:
    """Сохраняет данные о вакансиях и компаниях в базу данных"""
    conn = psycopg2.connect(dbname=name_database, **params)
    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                '''
                INSERT INTO company (company_name, address)
                VALUES (%s, %s)
                ''',
                (item['company_name'], item['company_address'])
            )

            cur.execute(
                '''
                INSERT INTO ads (
                ads_name, 
                data_published,
                requirement,
                responsibility)
                VALUES (%s, %s, %s, %s)
                ''',
                (item['ad_name'], item['published_at'], item['requirement'], item['responsibility'])
            )
    conn.commit()
    conn.close()
