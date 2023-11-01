from utils import get_employer_hh, get_vacancies_hh, create_database, save_vacancies_to_db, save_employers_to_db
from config import config
from db_manager import DBManager

employers_id = [78638, 1740, 84585, 3529, 3144945, 105904, 4949, 41862, 793926, 3776]


def main():
    params = config()

    create_database('headhunter', params)
    employers = get_employer_hh(employers_id)
    vacancies = get_vacancies_hh(employers_id)

    save_employers_to_db(employers, 'headhunter', params)
    save_vacancies_to_db(vacancies, 'headhunter', params)

    db_manager = DBManager('headhunter', params)

    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword()


if __name__ == '__main__':
    main()
