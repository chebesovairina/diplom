from config import *


# ---------------------------------------------------СОЗДАНИЕ РЕЗЮМЕ---------------------------------------------------
def create_new_resume(personal_info, education, work_experience, output_docx):
    text_resume = "ФИО: " + personal_info["full_name"] + '\n' + "email: " + personal_info[
                      "email"] + '\n' + "Номер телефона: " + personal_info["phone"] + "Должность: " + personal_info[
                      "vacancy"] + '\n' + "Навыки: " + personal_info["skills"] + '\n' + "Качества: " + personal_info[
                      "soft_skills"] + '\n'+ "Достижения: " + personal_info[
                      "achievements"] + '\n' + "Дополнительная информация: " + personal_info[
                      "additional_information"] + '\n' + "Образование: " + str(
        education) + '\n' + "Опыт работы: " + str(work_experience)

    # ---------------------------------------ПРОФИЛЬ---------------------------------------
    request_profile_summary_text = f'''
    Ты являешься профессиональным копирайтером, который умеет анализировать и обобщать прочитанную информацию.
    Перед тобой стоит задача - на основе введенных пользователем данных для его резюме создать необходимую информацию.
    Нужна информация:
    Описание профиля: В этом разделе в 2–3 предложениях следует обобщить профессиональный опыт, ключевые навыки и достижения.
    Это "визитная карточка" кандидата, дающая рекрутерам быстрый обзор его квалификации и амбиций.
    Расскажи о кандидате так, чтобы он мог заинтересовать работодателя.
    В качестве ответа верни только текст раздела, ничего больше писать не нужно.
    Вот текст резюме: {text_resume}
    '''
    profile_summary = prompt_api(request_profile_summary_text)

    # ---------------------------------------СКИЛЫ---------------------------------------
    request_skills_text = f'''
    Ты являешься профессиональным копирайтером, который умеет анализировать и обобщать прочитанную информацию.
    Перед тобой стоит задача - на основе введенных пользователем данных для его резюме создать необходимую информацию.
    Нужна информация:
    Кандидат указал свои скилы и навыки, проанализируй их и на их основе добавь как можно больше дополнительных навыков,
    чтобы кандидат был интересен работодателю и соответствовал должности {personal_info["vacancy"]})
    В качестве ответа верни все написанные тобой скилы в одну строчку через запятую, больше ничего не пиши.
    Вот текст резюме: {text_resume}
    '''
    skills = prompt_api(request_skills_text)

    # --------------------------------------КАЧЕСТВА--------------------------------------
    request_skills_text = f'''
    Ты являешься профессиональным копирайтером, который умеет анализировать и обобщать прочитанную информацию.
    Перед тобой стоит задача - на основе введенных пользователем данных для его резюме создать необходимую информацию.
    Нужна информация:
    Кандидат указал свои личностные качества, проанализируй их и на их основе добавь как можно больше дополнительных качеств,
    чтобы кандидат был интересен работодателю и соответствовал должности {personal_info["vacancy"]})
    В качестве ответа верни все написанные тобой качества в одну строчку через запятую, больше ничего не пиши.
    Вот текст резюме: {text_resume}
    '''
    soft_skills = prompt_api(request_skills_text)

    # ---------------------------------------РАБОТА---------------------------------------
    request_experience_text = f'''
    Ты являешься профессиональным копирайтером, который умеет анализировать и обобщать прочитанную информацию.
    Перед тобой стоит задача - на основе введенных пользователем данных для его резюме создать необходимую информацию.
    Нужна информация:
    Релевантный опыт работы (Среди всего опыта работы в компаниях выдели все варианты релевантного опыта работы для должности {personal_info["vacancy"]})
    В качестве ответа верни релевантный опыт работы, строго следуя следующему шаблону:
    [Название компании] | [Годы работы] | [Должность]
    [Краткое описание проделанной работы (создай краткое описание опыта работы сотрудника в данной компании)]
    [Список выполненных на должности задач (если не указан, создай минимум 5 задач, ориентируясь на данные о должности)]
    Не пиши заголовок, только текст, в соответствии с шаблоном.
    Вот текст опыта работы: {work_experience}
    '''
    experience = prompt_api(request_experience_text)

    # ---------------------------------------ОБРАЗОВАНИЕ---------------------------------------
    request_education_text = f'''
    Ты являешься профессиональным копирайтером, который умеет анализировать и обобщать прочитанную информацию.
    Перед тобой стоит задача - на основе введенных пользователем данных для его резюме создать необходимую информацию.
    Нужна информация:
    Образование (Среди всего указанного образования найди только тот, который относится к должности, на которую претендует сотрудник {personal_info["vacancy"]})
    В качестве ответа верни найденный тобой текст, строго следуя следующему шаблону:
    [Название учебного заведения] | [Годы учебы]
    [Специальность]
    Не пиши заголовок, только текст, в соответствии с шаблоном.
    Вот текст образования: {education}
    '''
    education = prompt_api(request_education_text)
    # Создание нового docx документа
    doc = Document()
    doc.styles['Normal'].font.name = 'Arial'
    doc.styles['Normal'].font.size = Pt(12)
    doc.styles['Normal'].font.bold = False

    paragraph = doc.add_paragraph()
    run = paragraph.add_run(f'{personal_info["full_name"]}')
    run.bold = True

    doc.add_paragraph(f'Email: {personal_info["email"]}')
    doc.add_paragraph(f'Телефон: {personal_info["phone"]}')

    paragraph = doc.add_paragraph()
    run_position_text = paragraph.add_run('Должность: ')
    run_job = paragraph.add_run(f'{personal_info["vacancy"]}')
    run_job.bold = True

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Описание профиля')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(profile_summary.strip())

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Навыки')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(skills.strip())

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Качества')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(soft_skills.strip())

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Опыт работы')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(experience.strip())

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Образование')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(education.strip())

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Достижения')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(f'{personal_info["achievements"]}')

    paragraph = doc.add_heading(level=2)
    run_position = paragraph.add_run('Дополнительная информация')
    run_position.font.color.rgb = RGBColor(42, 79, 150)
    paragraph = doc.add_paragraph()
    paragraph.add_run(f'{personal_info["additional_information"]}')

    doc.save(output_docx)


# ----------------------------------------------------АНАЛИЗ РЕЗЮМЕ----------------------------------------------------
def analyze_resume(filename, file_path):
    text = ""
    if filename.endswith('.pdf'):
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    elif filename.endswith('.docx'):
        original_doc = Document(file_path)
        for paragraph in original_doc.paragraphs:
            text += paragraph.text
    request_analyze_text = f'''
    Ты являешься профессиональным рекрутером, который много лет работал с резюме кандидатов.
    Твоя задача проверить текущее резюме на соответствие лучшим практикам, и дать рекомендации по улучшению.
    Согласно твоим данным резюме должно содержать следующие поля - ФИО, контактный номер телефона и email, название должности, описание профиля,
    релевантные образование и опыт работы, навыки, качества, достижения и дополнительная информация.
    Оценивай резюме с точки зрения выбранной должности. Учти, что кандидат может быть студентом и не иметь опыта работы.
    В качестве ответа верни рекомендации по улучшению данного резюме.
    Вот текст резюме: {text}
    '''
    analyze = prompt_api(request_analyze_text)

    request_result_text = f'''
    Ты являешься профессиональным рекрутером, который много лет работал с резюме кандидатов.
    Ты получил от кандидата резюме, а также рекомендации по улучшению данного резюме: {analyze}.
    Твоя задача следуя рекомендациям предложить вариант улучшения данного резюме.
    Составь свой ответ следуя требованиям и рекомендациям. Если каких-то разделов не хватает дополни их самостоятельно,
    или укажи необходимость этого кандидату, не пропускай ни один раздел. Исходную информацию бери из исходного резюме кандидата.
    Вот текст исходного резюме кандидата: {text}
    Твой ответ должен строго соответствовать формату, а также не иметь никаких выделений:
    ФИО:
    Номер телефона:
    Email:
    Должность:
    Описание профиля:
    Навыки:
    Качества:
    Образование:
    Опыт работы:
    Достижения:
    Дополнительная информация:
    '''
    result = prompt_api(request_result_text)

    resume_sections = {}
    pattern = r"^\s*(ФИО|Номер телефона|Email|Должность|Описание профиля|Навыки|Качества|Образование|Опыт работы|Достижения|Дополнительная информация):\s*(.*?)\s*(?=\n\s*(?:ФИО|Номер телефона|Email|Должность|Описание профиля|Навыки|Образование|Опыт работы|Достижения|Дополнительная информация)|\Z)"
    all_sections_found = True
    try:
        # Ищем все разделы и их содержимое
        matches = re.findall(pattern, result, re.MULTILINE | re.DOTALL)
        # Проверка, удалось ли найти все разделы
        expected_sections = ["ФИО", "Номер телефона", "Email", "Должность", "Описание профиля",
                             "Навыки", "Качества", "Образование", "Опыт работы", "Достижения", "Дополнительная информация"]
        found_sections = set(section for section, _ in matches)
        # Если отсутствуют какие-либо разделы, ставим флаг в False
        if not found_sections.issuperset(expected_sections):
            all_sections_found = False
        # Сохраняем разделы, если все они найдены
        if all_sections_found:
            for section, content in matches:
                resume_sections[section] = content.strip()
    except Exception as e:
        print(f"Произошла ошибка при извлечении разделов: {e}")
        all_sections_found = False

    # Создаем новый документ Word
    doc = Document()
    doc.styles['Normal'].font.name = 'Arial'
    doc.styles['Normal'].font.size = Pt(12)
    doc.styles['Normal'].font.bold = False

    doc.add_heading("Анализ резюме", level=1)
    doc.add_paragraph(f'{analyze}')

    if all_sections_found:
        paragraph = doc.add_paragraph()
        run = paragraph.add_run(f'{resume_sections["ФИО"]}')
        run.bold = True
        doc.add_paragraph(f'Email: {resume_sections["Email"]}')
        doc.add_paragraph(f'Телефон: {resume_sections["Номер телефона"]}')
        doc.add_paragraph(f'Должность: {resume_sections["Должность"]}')

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Описание профиля')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Описание профиля"])

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Навыки')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Навыки"])

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Образование')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Образование"])

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Опыт работы')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Опыт работы"])

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Достижения')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Достижения"])

        paragraph = doc.add_heading(level=2)
        run_position = paragraph.add_run('Дополнительная информация')
        run_position.font.color.rgb = RGBColor(42, 79, 150)
        paragraph = doc.add_paragraph()
        paragraph.add_run(resume_sections["Дополнительная информация"])

    else:
        # Если разделы не найдены или есть ошибка, добавляем текст без форматирования
        paragraph = doc.add_paragraph()
        paragraph.add_run(result)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", analyze)
    return html_text


# ---------------------------------------------СРАВНЕНИЕ РЕЗЮМЕ С ВАКАНСИЕЙ---------------------------------------------
def compare_resume_with_vacancy(vacancy_text, filename, resume_path):
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
    Твоя задача проанализировать текущее резюме кандидата и определить соответствие кандидата с данным резюме для работы на заданной вакансии.
    Учитывай рекомендуемые для данной вакансии опыт работы, навыки и другую необходимую информацию.
    Если информации в тексте вакансии недостаточно - ориентируйся на текущие практики на рынке для заданной вакансии.
    Для начала дай количественную оценку соответствия от 0 до 100%.
    После количественной оценки приведи краткое пояснение своего выбора - 2-3 предложения.
    Далее предложи кандидату возможности улучшения навыков или опыта работы, если считаешь это необходимым.
    Вот текст вакансии, на которую претендует кандидат: {vacancy_text}
    Вот текст резюме: {text}
    '''
    result_text = prompt_api(request_analyze_text)
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result_text)
    return html_text