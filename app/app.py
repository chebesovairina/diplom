from config import *
from database import *
from HH_ru import *
from keywords import *
from career_func import *
from resume_func import *
from interview_func import *
from bot_reply import *

# Запускаем базу данных перед стартом приложения
init_db()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        email = request.form.get('email')
        password = request.form.get('password')
        password_rep = request.form.get('password_proof')
        user = check_data(email)
        if password != password_rep:
            return render_template('register.html', error_message="Пароли должны совпадать.")
        if user:
            return render_template('register.html', error_message="Пользователь с таким email уже зарегистрирован.")
        else:
            add_data(email, password)
            user = check_data(email)
            session['user_id'] = user[0]
        return redirect(url_for('main'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_id = check_login(email, password)
        if not user_id:
            return render_template('log_in.html', error_message="Неверный логин или пароль.")
        else:
            session['user_id'] = user_id
            return redirect(url_for('main'))
    return render_template('log_in.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем id пользователя из сессии
    return redirect(url_for('welcome'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    bot_reply = get_bot_reply("profile")
    user_id = session['user_id']
    avatars = ["avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png", "avatar5.png", "avatar6.png", "avatar7.png", "avatar8.png", "avatar9.png"]  # Доступные аватарки
    if request.method == 'POST':
        selected_avatar = request.form.get('avatar')
        if selected_avatar in avatars:
            update_avatar(user_id, selected_avatar)
            return redirect(url_for('profile'))  # Обновление страницы
    return render_template('profile.html', current_avatar=get_current_avatar(), avatars=avatars, bot_reply=bot_reply)

@app.route('/main')
def main():
    bot_reply = get_bot_reply("main")
    return render_template('main.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)


@app.route('/career')
def career():
    bot_reply = get_bot_reply("career")
    return render_template('career.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/career/test', methods=['GET', 'POST'])
def career_test():
    bot_reply = get_bot_reply("career_test")
    pairs = [
        ("Автомеханик", "Физиотерапевт"),
        ("Специалист по защите информации", "Логистик"),
        ("Оператор связи", "Кинооператор"),
        ("Водитель", "Продавец"),
        ("Инженер-конструктор", "Менеджер по продажам"),
        ("Диспетчер", "Дизайнер компьютерных программ"),
        ("Ветеринар", "Эколог"),
        ("Биолог-исследователь", "Фермер"),
        ("Лаборант", "Дрессировщик"),
        ("Агроном", "Санитарный врач"),
        ("Селекционер", "Заготовитель сельхозпродуктов"),
        ("Микробиолог", "Ландшафтный дизайнер"),
        ("Массажист", "Воспитатель"),
        ("Преподаватель", "Предприниматель"),
        ("Администратор", "Режиссер театра и кино"),
        ("Официант", "Врач"),
        ("Психолог", "Торговый агент"),
        ("Страховой агент", "Хореограф"),
        ("Ювелир-гравер", "Журналист"),
        ("Искусствовед", "Продюсер"),
        ("Редактор", "Музыкант"),
        ("Дизайнер интерьера", "Экскурсовод"),
        ("Композитор", "Арт-директор"),
        ("Музейный работник", "Актер театра и кино"),
        ("Верстальщик", "Гид-переводчик"),
        ("Лингвист", "Антикризисный управляющий"),
        ("Корректор", "Художественный редактор"),
        ("Наборщик текстов", "Юрисконсульт"),
        ("Программист", "Брокер"),
        ("Бухгалтер", "Литературный переводчик"),
    ]

    # Таблица соответствий
    mapping = [
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
        ('р', 'с'), ('и', 'п'), ('о', 'а'),
    ]
    if request.method == 'POST':
        results = request.form  # Считываем ответы пользователя
        # Инициализация счетчика баллов
        scores = {'р': 0, 'и': 0, 'с': 0, 'о': 0, 'п': 0, 'а': 0}
        # Обработка ответов
        for i, choice in enumerate(results.values()):
            # choice — выбранная профессия
            left_type, right_type = mapping[i]
            if choice == pairs[i][0]:  # Если выбрана левая профессия
                scores[left_type] += 1
            elif choice == pairs[i][1]:  # Если выбрана правая профессия
                scores[right_type] += 1
        # Определение результата
        # Структура данных для передачи: каждый тип и его баллы
        output = {
            'р': scores['р'],
            'и': scores['и'],
            'с': scores['с'],
            'о': scores['о'],
            'п': scores['п'],
            'а': scores['а']
        }
        # Анализируем результаты
        sorted_descriptions = analyse_career_test(output)
        result_text = sorted_descriptions[0][1] + '\n\n' + dop_career_test(sorted_descriptions[0][1])
        bot_reply = get_bot_reply("career_test_result")
        # Возвращаем результаты в шаблон
        return render_template('career_test_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('career_test.html', pairs=pairs, enumerate=enumerate, current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/career/test/result')
def career_test_result():
    return render_template('career_test_result.html', current_avatar=get_current_avatar())

@app.route('/career/analysis', methods=['GET', 'POST'])
def career_analysis():
    bot_reply = get_bot_reply("career_analysis")
    if request.method == 'POST':
        career_name = request.form.get('career_analysis')
        vacancies = get_vacancies_for_career(career_name)
        result_text = analyse_career(career_name, vacancies)
        bot_reply = get_bot_reply("career_analysis_result", career_name=career_name)
        return render_template('career_analysis_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('career_analysis.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/career/analysis/result')
def career_analysis_result():
    return render_template('career_analysis_result.html', current_avatar=get_current_avatar())

@app.route('/career/selection', methods=['GET', 'POST'])
def career_selection():
    bot_reply = get_bot_reply("career_selection")
    if request.method == 'POST':
        # Проверяем, загружен ли файл
        if 'resume_file' not in request.files:
            return render_template('career_selection.html', error_message="Пожалуйста, загрузите файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        file = request.files['resume_file']
        # Проверяем расширение файла
        if file.filename == '':
            return render_template('career_selection.html', error_message="Файл не выбран.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        if not allowed_file(file.filename):
            return render_template('career_selection.html',
                                   error_message="Неверный формат. Загрузите PDF или DOCX файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        # Сохраняем загруженный файл в папку Загрузки
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        resume_text = ""
        # Вызываем функцию анализа в зависимости от формата
        if file.filename.endswith('.pdf'):
            with open(upload_path, "rb") as file:
                reader = PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    resume_text += page.extract_text()
        elif file.filename.endswith('.docx'):
            original_doc = Document(upload_path)
            for paragraph in original_doc.paragraphs:
                resume_text += paragraph.text
        full_text = resume_text
        keywords = extract_keywords(full_text)
        save_keywords(str(session.get('user_id', '')), keywords)
        vacancies = get_vacancies(keywords)
        result_text = select_career(file.filename, upload_path, vacancies)
        # Отправляем обработанный файл пользователю
        bot_reply = get_bot_reply("career_selection_result", keywords=keywords)
        return render_template('career_selection_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('career_selection.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/career/selection/result')
def career_selection_result():
    return render_template('resume_vacancy_result.html', current_avatar=get_current_avatar())


@app.route('/resume')
def resume():
    bot_reply = get_bot_reply("resume")
    return render_template('resume.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/resume/creating', methods=['GET', 'POST'])
def create_resume():
    bot_reply = get_bot_reply("resume_creating")
    if request.method == 'POST':
        personal_info = {
            "full_name": request.form.get("full_name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "vacancy": request.form.get("vacancy"),
            "skills": request.form.get("skills"),
            "soft_skills": request.form.get("soft_skills"),
            "achievements": request.form.get("achievements"),
            "additional_information": request.form.get("additional_information"),
        }
        # Получаем массивы данных об образовании и опыте работы
        education = request.form.getlist("education")
        work_experience = request.form.getlist("work_experience")
        # Создаем временный файл для резюме
        output_path = "resume.docx"
        create_new_resume(personal_info, education, work_experience, output_path)
        # Отправляем обработанный файл пользователю
        return send_file(output_path, as_attachment=True)
    return render_template('resume_creating.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/resume/analysis', methods=['GET', 'POST'])
def resume_analysis():
    bot_reply = get_bot_reply("resume_analysis")
    if request.method == 'POST':
        # Проверяем, загружен ли файл
        if 'resume_file' not in request.files:
            return render_template('resume_analysis.html', error_message="Пожалуйста, загрузите файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        file = request.files['resume_file']
        # Проверяем расширение файла
        if file.filename == '':
            return render_template('resume_analysis.html', error_message="Файл не выбран.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        if not allowed_file(file.filename):
            return render_template('resume_analysis.html', error_message="Неверный формат. Загрузите PDF или DOCX файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        # Сохраняем загруженный файл в папку Загрузки
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        resume_text = ""
        # Вызываем функцию анализа в зависимости от формата
        if file.filename.endswith('.pdf'):
            with open(upload_path, "rb") as file:
                reader = PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    resume_text += page.extract_text()
        elif file.filename.endswith('.docx'):
            original_doc = Document(upload_path)
            for paragraph in original_doc.paragraphs:
                resume_text += paragraph.text
        full_text = resume_text
        keywords = extract_keywords(full_text)
        save_keywords(str(session.get('user_id', '')), keywords)
        result_text = analyze_resume(file.filename, upload_path)
        # Отправляем обработанный файл пользователю
        bot_reply = get_bot_reply("resume_analysis_result", keywords=keywords)
        return render_template('resume_analysis_result.html', result_text=result_text,
                               current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('resume_analysis.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/resume/analysis/result')
def resume_analysis_result():
    return render_template('resume_analysis_result.html', current_avatar=get_current_avatar())

@app.route('/resume/vacancy', methods=['GET', 'POST'])
def resume_vacancy():
    bot_reply = get_bot_reply("resume_vacancy")
    if request.method == 'POST':
        vacancy_text = request.form.get('vacancy_text')
        file = request.files['resume_file']
        if not vacancy_text or not file or not allowed_file(file.filename):
            return render_template('resume_vacancy.html', error_message="Введите текст вакансии и загрузите PDF или DOCX файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        filename = secure_filename(file.filename)
        resume_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(resume_path)
        resume_text = ""
        if file.filename.endswith('.pdf'):
            with open(resume_path, "rb") as file:
                reader = PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    resume_text += page.extract_text()
        elif file.filename.endswith('.docx'):
            original_doc = Document(resume_path)
            for paragraph in original_doc.paragraphs:
                resume_text += paragraph.text
        full_text = resume_text + "\n" + vacancy_text
        keywords = extract_keywords(full_text)
        save_keywords(str(session.get('user_id', '')), keywords)
        result_text = compare_resume_with_vacancy(vacancy_text, filename, resume_path)
        bot_reply = get_bot_reply("resume_vacancy_result", keywords=keywords)
        return render_template('resume_vacancy_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('resume_vacancy.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/resume/vacancy/result')
def resume_vacancy_result():
    return render_template('resume_vacancy_result.html', current_avatar=get_current_avatar())


@app.route('/interview')
def interview():
    bot_reply = get_bot_reply("interview")
    return render_template('interview.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/interview/advice', methods=['GET', 'POST'])
def interview_advice():
    bot_reply = get_bot_reply("interview_advice")
    if request.method == 'POST':
        career_name = request.form.get('career_name')
        vacancies = get_vacancies_for_career(career_name)
        result_text = advice_interview(career_name, vacancies)
        bot_reply = get_bot_reply("interview_advice_result", career_name=career_name)
        return render_template('interview_advice_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('interview_advice.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/interview/advice/result')
def interview_advice_result():
    return render_template('interview_advice_result.html', current_avatar=get_current_avatar())

@app.route('/interview/question', methods=['GET', 'POST'])
def interview_question():
    bot_reply = get_bot_reply("interview_question")
    if request.method == 'POST':
        vacancy_text = request.form.get('vacancy_text')
        full_text = vacancy_text
        keywords = extract_keywords(full_text)
        save_keywords(str(session.get('user_id', '')), keywords)
        vacancies = get_vacancies(keywords)
        result_text = question_interview(vacancy_text, vacancies)
        bot_reply = get_bot_reply("interview_question_result", keywords=keywords)
        return render_template('interview_question_result.html', result_text=result_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('interview_question.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/interview/question/result')
def interview_question_result():
    return render_template('interview_question_result.html', current_avatar=get_current_avatar())

@app.route('/interview/try', methods=['GET', 'POST'])
def interview_try():
    bot_reply = get_bot_reply("interview_try")
    if request.method == 'POST':
        vacancy_text = request.form.get('vacancy_text')
        file = request.files['resume_file']
        if not vacancy_text or not file or not allowed_file(file.filename):
            return render_template('interview_try.html', error_message="Введите текст вакансии и загрузите PDF или DOCX файл.", current_avatar=get_current_avatar(), bot_reply=bot_reply)
        filename = secure_filename(file.filename)
        resume_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(resume_path)
        interview_text = create_interview_text(vacancy_text, filename, resume_path)
        bot_reply = get_bot_reply("interview_try_answers")
        return render_template('interview_try_answers.html', interview_text=interview_text, filename=filename, resume_path=resume_path, vacancy_text=vacancy_text, current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('interview_try.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/interview/try/answers', methods=['GET', 'POST'])
def interview_try_answers():
    bot_reply = get_bot_reply("interview_try_answers")
    if request.method == 'POST':
        vacancy_text = request.form.get("vacancy_text")
        filename = request.form.get("filename")
        resume_path = request.form.get("resume_path")
        answers = request.form.get('answers_text')
        interview_text = request.form.get('interview_text')
        result_text = analysis_interview_answers(answers, interview_text, vacancy_text, filename, resume_path)
        resume_text = ""
        if filename.endswith('.pdf'):
            with open(resume_path, "rb") as file:
                reader = PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    resume_text += page.extract_text()
        elif filename.endswith('.docx'):
            original_doc = Document(resume_path)
            for paragraph in original_doc.paragraphs:
                resume_text += paragraph.text
        full_text = resume_text + "\n" + vacancy_text
        keywords = extract_keywords(full_text)
        save_keywords(str(session.get('user_id', '')), keywords)
        bot_reply = get_bot_reply("interview_try_answers_result", keywords=keywords)
        return render_template('interview_try_answers_result.html', result_text=result_text,
                               current_avatar=get_current_avatar(), bot_reply=bot_reply)
    return render_template('interview_try_answers.html', current_avatar=get_current_avatar(), bot_reply=bot_reply)

@app.route('/interview/try/answers/result')
def interview_try_answers_result():
    return render_template('interview_try_answers_result.html', current_avatar=get_current_avatar())

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
