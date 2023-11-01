import requests
import psycopg2
from db_manager import DBManager


def get_employer_hh(employers_id):
    """ Получение данных о работодателе по АПИ ХХ."""
    data = []
    employers_data = []
    for employer_id in employers_id:
        params = {'per_page': 50}
        hh_url_employers = f'https://api.hh.ru/employers/{employer_id}'
        response = requests.get(hh_url_employers, params=params)
        items = response.json()
        data.append(items)
        for item in data:
            employer_id = item['id']
            company_name = item['name']
          #  employers_data.append({
           #     'employer_id': item['id'],
           #     'company_name': item['name'],
           #     'url': item['vacancies_url']
           # })
            employers_data.append([employer_id, company_name])
    return employers_data


def get_vacancies_hh(vacancies):
    """
    Получение данных о вакансии по апи.
    """
    vacancies_data = []
    for employer_id in vacancies:
        params = {'per_page': 50}
        hh_url_vacancies = f'https://api.hh.ru/vacancies?employer_id={employer_id}'
        response = requests.get(hh_url_vacancies, params=params)
        items = response.json()['items']
        for item in items:
            salary = item['salary']
            vacancy_id = item['id'],
            vacancy_name = item['name'],
            salary_from = 0 if salary is None or salary['from'] is None else salary['from'],
            salary_to = 0 if salary is None or salary['to'] is None else salary['to'],
            requirement = item['snippet']['requirement'],
            vacancy_url = item['alternate_url'],
            employer_id = item['employer']['id']
            #vacancies_data.append({
            #    'vacancy_id': item['id'],
             #   'vacancy_name': item['name'],
             #   'salary_from': 0 if salary is None or salary['from'] is None else salary['from'],
             #   'salary_to': 0 if salary is None or salary['to'] is None else salary['to'],
              #  'requirement': item['snippet']['requirement'],
              #  'vacancy_url': item['alternate_url'],
             #   'employer_id': item['employer']['id']
           # })
            vacancies_data.append([vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url, employer_id])
    return vacancies_data


def create_database(database_name, params):
    """Создание базы данных и таблиц для сохранения данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                company_name VARCHAR(50) NOT NULL
            )        
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR,
                salary_from INTEGER,
                salary_to INTEGER,
                requirement TEXT,
                vacancy_url TEXT,
                employer_id INTEGER REFERENCES employers(employer_id) 
            )
        """)
    conn.commit()
    conn.close()

def save_employers_to_db(data, database_name, params):
    """Заполнение таблицы employers данными о компаниях"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for employer in data:
            query = "INSERT INTO employers (employer_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
            cur.execute(query, employer)
    conn.commit()
    conn.close()


def save_vacancies_to_db(data, database_name, params):
    """Заполнение таблицы vacancies данными о вакансиях"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in data:
            query = "INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url, employer_id) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, vacancy)
    conn.commit()
    conn.close()

