import psycopg2


class VacancyCompanyHh:
    """Класс для получения данных с таблиц Company, Ads """
    def __init__(self, data_base_name, params: dict):
        self.data_base_name = data_base_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.data_base_name, **self.params)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute('''SELECT DISTINCT company_name, COUNT(ads_name) FROM company
                            INNER JOIN ads USING(company_id) GROUP BY company_name'''
                        )

            result = cur.fetchall()
            dct_result = dict(result)
        return dct_result

    def get_all_vacancies(self):
        """Получает список всех вакансий с названием компании, названием вакансии, зарплатой и ссылкой на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute(''' SELECT company_name, ads_name, salary_from, salary_to, url FROM ads
                            FULL JOIN company USING(company_id)''')
            result = cur.fetchall()
            return result

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute('''SELECT AVG(salary_from) FROM ads''')
            result = cur.fetchall()
            return result

    def get_vacancies_with_keyword(self, key_word):
        """Получает список вакансий по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute(f'''SELECT * FROM ads WHERE ads_name = %s''', (key_word,))
            result = cur.fetchall()
            return result
