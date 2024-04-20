import psycopg2


class GetDataFromDataBase:

    def get_data_from_database(self):
        conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        conn.autocommit = True
        data = []
        with conn.cursor() as cur:
            cur.execute('SELECT company_name,  FROM company;')
            vacancy_data = cur.fetchall()
            data.append(vacancy_data)
            return data


class VacancyCompanyHh:
    def __init__(self, data_base_name, params: dict):
        self.data_base_name = data_base_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        self.conn.autocommit = True
        self.mag = 'МАГНИТ'
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute(
                f'SELECT DISTINCT company_name, COUNT(ads_name) FROM company '
                f'INNER JOIN ads USING(company_id) WHERE company_name IN ({self.mag}) GROUP BY company_name')

            result = cur.fetchall()
            return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с названием компании, названием вакансии, зарплатой и ссылкой на вакансию"""
        pass

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список вакансий по ключевому слову"""
        pass
