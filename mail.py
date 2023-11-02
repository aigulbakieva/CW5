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
    while True:
        print('''
        Добрый день!
        Выберите один из пунктов:
        1 - получить список всех вакансий и количество вакансий у каждой компании
        2 - получить cписок всех вакансий с указанием всей информации о вакансии
        3 - получить среднюю зарплату по всем вакансиям 
        4 - получить вакансии, у которых зарплата выше средней по всем вакансиям 
        5 - получить список вакансий, в названии которых содержится слово Python
        0 - выход''')

        user_input = input()
        if user_input == '1':
            db_manager.get_companies_and_vacancies_count()
        elif user_input == '2':
            db_manager.get_all_vacancies()
        elif user_input == '3':
            db_manager.get_avg_salary()
        elif user_input == '4':
            db_manager.get_vacancies_with_higher_salary()
        elif user_input == '5':
            db_manager.get_vacancies_with_keyword()
        elif user_input == '0':
            break
        else:
            print('Неверный запрос')


if __name__ == '__main__':
    main()
