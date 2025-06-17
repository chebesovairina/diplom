from config import *

def extract_keywords(text):
    request_analyze_text = f"""
        Ты — аналитик текстов вакансий и резюме. Твоя задача — извлекать ключевые слова строго по следующим категориям:

        - job_titles: Названия вакансий
        - companies: Названия компаний
        - skills: Навыки и технологии (языки программирования, фреймворки, базы данных, инструменты)
        - languages: Иностранные языки
        - other: Другие полезные ключевые слова для поиска работы

        **Важно:** 
        - Ответ должен быть в формате JSON.
        - Поля должны содержать списки строк (даже если найдено одно значение).
        - При формировании ключевых слов избегай наличия любых знаков (таких как тире, запятая и тд.).
        - Если категория пустая, верни пустой список `[]`, но не пропускай поле.

        Текст для анализа:
        {text}

        Выведи только JSON без пояснений и дополнительного текста.
    """
    text_response = prompt_api(request_analyze_text)
    try:
        clean_response = re.sub(r"^```|```$", "", text_response.strip()).strip()
        parsed_response = json.loads(clean_response)  # Конвертируем в JSON
        return parsed_response
    except json.JSONDecodeError:
        parsed_response = {}  # Если ошибка, возвращаем пустой объект
        return parsed_response


def save_keywords(user_id, keywords):
    if keywords == {}:
        return
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Проверяем, есть ли уже запись для данного user_id
    cursor.execute("SELECT job_titles, companies, skills, languages, other FROM user_vacancies WHERE user_id = ?",
                   (user_id,))
    existing_data = cursor.fetchone()
    if existing_data:
        # Если запись уже есть, дополняем ключевые слова
        updated_data = {
            "job_titles": set(existing_data[0].split(", ") + keywords.get("job_titles", [])),
            "companies": set(existing_data[1].split(", ") + keywords.get("companies", [])),
            "skills": set(existing_data[2].split(", ") + keywords.get("skills", [])),
            "languages": set(existing_data[3].split(", ") + keywords.get("languages", [])),
            "other": set(existing_data[4].split(", ") + keywords.get("other", [])),
        }
        # Обновляем запись
        cursor.execute("""
            UPDATE user_vacancies
            SET job_titles = ?, companies = ?, skills = ?, languages = ?, other = ?
            WHERE user_id = ?
        """, (
            ", ".join(updated_data["job_titles"]),
            ", ".join(updated_data["companies"]),
            ", ".join(updated_data["skills"]),
            ", ".join(updated_data["languages"]),
            ", ".join(updated_data["other"]),
            user_id
        ))
    else:
        # Если записи нет, создаем новую
        cursor.execute("""
            INSERT INTO user_vacancies (user_id, job_titles, companies, skills, languages, other)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            ", ".join(keywords.get("job_titles", [])),
            ", ".join(keywords.get("companies", [])),
            ", ".join(keywords.get("skills", [])),
            ", ".join(keywords.get("languages", [])),
            ", ".join(keywords.get("other", []))
        ))
    conn.commit()
    conn.close()
