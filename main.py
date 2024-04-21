from pprint import pprint
from src.utils import save_data_to_database
from src.utils import create_data_base
from src.config import config
from src.utils import get_data_from_hh
from src.hh_class import VacancyCompanyHh\

# список id компаний для получения данных с headhunter
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
# переменная с конфигурацией для входа в базу данных
params = config()

# блок для получения данных с api headhunter, создания базы данных и таблиц,
# сохранения данных полученных с api в созданные таблицы
data_from_hh = get_data_from_hh(id_company_hh)
create_data_base('headhunter', params)
save_data_to_database(data_from_hh, 'headhunter', params)

# блок для проверки работы методов класса VacancyCompanyHh
inf_for_data_base = VacancyCompanyHh('headhunter', params)
full_inf_about_ads = inf_for_data_base.get_all_vacancies()
inf_about_count_vacancy = inf_for_data_base.get_companies_and_vacancies_count()
for k, v in inf_about_count_vacancy.items():
    print(f'Компания {k}, вакансий {v}')
pprint(full_inf_about_ads)
avg_salary = inf_for_data_base.get_avg_salary()
print(round(avg_salary[0][0]))
user_input = input()
search_by_keyword = inf_for_data_base.get_vacancies_with_keyword(user_input)
print(search_by_keyword)
