# Курсовая работа по базе данных

В данном проекте реализовано:
- Получение данных с api HeadHunter
- создание базы данных при помощи СУБД PostgreSQL
- создание таблиц Company(company_id, company_name) Ads(company_id, ads_name, salary_from, salary_to, url)
  - создан класс VacancyCompanyHh с методами основанными на командах СУБД postgreSQL для получения данных с базы данных

## Требования
- python 3.10^
- psycopg2
- requests

## Установка
`pip install psycopg-binary`
`pip install requests`
`sudo apt install python 3.10.12`