import psycopg2


class DBManager:

    def __init__(self, database, params):
        self.dbname = database
        self.params = params
        self.conn = psycopg2.connect(dbname=database, **params)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
                SELECT employers.company_name, COUNT(vacancies.employer_id) AS vacancy_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.company_name;
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            for company_name, vacancy_count in result:
                print(f'Компания: {company_name}, количество вакансий : {vacancy_count}')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        query = """
                SELECT employers.company_name, vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url FROM vacancies
                LEFT JOIN employers USING(employer_id)
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            for company_name, vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url in result:
                print(f'Компания: {company_name}, номер вакансии: {vacancy_id}, название вакансии: {vacancy_name},'
                      f' зарплата от: {salary_from}, зарплата до: {salary_to}, описание вакансии: {requirement}, ссылка: {vacancy_url}')
    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = """
                SELECT AVG((salary_from + salary_to)/2) AS avg_salary
                FROM vacancies
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            print(f'Средняя зарплата : {result}')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        query = """
                SELECT * FROM vacancies
                WHERE ((salary_from + salary_to)/2) >
                (SELECT AVG((salary_from + salary_to)/2) FROM vacancies)
                ORDER BY salary_from
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            for vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url, employer_id in result:
                print(f'Номер вакансии: {vacancy_id}, название вакансии: {vacancy_name},'
                      f' зарплата от: {salary_from}, зарплата до: {salary_to}, описание вакансии: {requirement}, ссылка: {vacancy_url}, id компании: {employer_id}')


    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        query = """
                SELECT * FROM vacancies
                WHERE vacancy_name LIKE '%Python%' OR requirement LIKE '%Python%'
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            for vacancy_id, vacancy_name, salary_from, salary_to, requirement, vacancy_url, employer_id in result:
                print(f'Номер вакансии: {vacancy_id}, название вакансии: {vacancy_name},'
                      f' зарплата от: {salary_from}, зарплата до: {salary_to}, описание вакансии: {requirement}, ссылка: {vacancy_url}, id компании: {employer_id}')

