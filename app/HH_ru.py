from config import *


def get_vacancies(keywords, per_page=10):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    if keywords == {}:
        all_vacancies.append("Не удалось найти вакансии, не используй эти данные")
        return all_vacancies
    for job_title in keywords["job_titles"]:
        params = {
            "text": f'NAME:{job_title}',
            "per_page": per_page,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            vacancies = response.json().get("items", [])
            for v in vacancies:
                salary_info = v.get("salary")
                if salary_info:
                    salary = f"{salary_info.get('from', 'Не указано')} - {salary_info.get('to', 'Не указано')} {salary_info.get('currency', '')}"
                else:
                    salary = "Не указано"
                vacancy_data = {
                    "title": v.get("name"),
                    "url": v.get("alternate_url"),
                    "company": v.get("employer", {}).get("name"),
                    "experience": v.get("experience", {}).get("name"),
                    "work_format": v.get("schedule", {}).get("name"),
                    "salary": salary,
                    "requirements": v.get("snippet", {}).get("requirement"),
                    "responsibilities": v.get("snippet", {}).get("responsibility"),
                }
                all_vacancies.append(vacancy_data)
        else:
            print(f"Ошибка при запросе вакансий: {response.status_code}")
    return all_vacancies


def get_vacancies_for_career(career, area=1, per_page=10):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    params = {
        "text": f'NAME:{career}',
        "per_page": per_page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies = response.json().get("items", [])
        for v in vacancies:
            salary_info = v.get("salary")
            if salary_info:
                salary = f"{salary_info.get('from', 'Не указано')} - {salary_info.get('to', 'Не указано')} {salary_info.get('currency', '')}"
            else:
                salary = "Не указано"
            vacancy_data = {
                "title": v.get("name"),
                "url": v.get("alternate_url"),
                "company": v.get("employer", {}).get("name"),
                "experience": v.get("experience", {}).get("name"),
                "work_format": v.get("schedule", {}).get("name"),
                "salary": salary,
                "requirements": v.get("snippet", {}).get("requirement"),
                "responsibilities": v.get("snippet", {}).get("responsibility"),
            }
            all_vacancies.append(vacancy_data)
    else:
        print(f"Ошибка при запросе вакансий: {response.status_code}")
    return all_vacancies
