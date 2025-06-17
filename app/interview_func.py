from config import *


def advice_interview(career_name, vacancies):
    request_analyze_text = f'''
    Ты являешься профессиональным рекрутером, который много лет работает в различных сферах найма персонала.
    Твоя задача проанализировать данную тебе сферу деятельности: {career_name}.
    Если данное название не соотносится ни с одной знакомой тебе рабочей сферой верни следующее сообщение:
    Извините, нам не удалось найти информацию о данной сфере, попробуйте другое название.
    Иначе, дай рекомендации по тому, как себя вести, что ожидать и как одеваться на собеседование согласно текущим
    трендам. Можешь также добавить другие разделы по желанию.
    Используй также информацию, полученную с сайта HeadHunter по выбранной сфере: {vacancies}
    '''
    result_text = prompt_api(request_analyze_text)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result_text)
    return html_text


def question_interview(vacancy_text, vacancies):
    request_analyze_text = f'''
    Ты являешься профессиональным рекрутером, который много лет работает в различных сферах найма персонала.
    Твоя задача проанализировать данную тебе вакансию: {vacancy_text}.
    Составь типичный список вопросов, соответствующий данной вакансии на собеседовании согласно текущим
    трендам. Важно! На каждый составленный тобой вопрос предоставь пример ответа с пояснением!
    Постарайся сделать их разнообразными, как на реальном собеседовании, чтобы кандидат понимал, чего ожидать.
    Используй также информацию, полученную с сайта HeadHunter по выбранной вакансии: {vacancies}
    '''
    result_text = prompt_api(request_analyze_text)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result_text)
    return html_text


def create_interview_text(vacancy_text, filename, resume_path):
    text = ""
    if filename.endswith('.pdf'):
        with open(resume_path, "rb") as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    elif filename.endswith('.docx'):
        original_doc = Document(resume_path)
        for paragraph in original_doc.paragraphs:
            text += paragraph.text
    request_analyze_text = f'''
    Ты являешься профессиональным рекрутером, который много лет работал с резюме кандидатов.
    Твоя задача подготовить 5 вопросов кандидату основываясь на тексте вакансии и резюме кандидата, чтобы оценить его профессиональные и личные навыки при устройстве на данную вакансию.
    Перед вопросами напиши небольшое вступление как будто пишешь рассказ от лица работодателя на собеседовании. Не отвечай на вопросы, твоя задача только задать их.
    Вот текст вакансии, на которую претендует кандидат: {vacancy_text}
    Вот текст резюме: {text}
    '''
    result_text = prompt_api(request_analyze_text)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result_text)
    return html_text


def analysis_interview_answers(answers, interview_text, vacancy_text, filename, resume_path):
    text = ""
    if filename.endswith('.pdf'):
        with open(resume_path, "rb") as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    elif filename.endswith('.docx'):
        original_doc = Document(resume_path)
        for paragraph in original_doc.paragraphs:
            text += paragraph.text
    request_analyze_text = f'''
    Ты являешься профессиональным рекрутером, имеющий большой опыт в оценке собеседований..
    Твоя задача проанализировать ответы кандидата на вопросы в процессе собеседования.
    Дай ответ в следующем виде для каждого вопроса в отдельности:
    Текст вопроса
    Оценка: дай качественную оценку ответа кандидата с точки зрения профессионала, укажи на сильные и слабые стороны ответа
    Пример: дай пример лучшего ответа на данный вопрос с точки зрения профессионала

    Вот текст собеседования, который содержит заданные кандидату вопросы: {interview_text}
    Вот текст ответа кандидата на вопросы: {answers}
    Вот текст вакансии, на которую претендует кандидат: {vacancy_text}
    Вот текст резюме: {text}
    '''
    result_text = prompt_api(request_analyze_text)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result_text)
    return html_text