# CHANGELOG — FitTrack

Проверочная работа курса «Создание веб-приложений на Flask».
Заполнены заготовки проекта под автотесты (`tests/`).

## Стек (зафиксирован в requirements.txt — не менять)

- flask==2.0.2, werkzeug==2.0.2
- flask-sqlalchemy==2.5.1, sqlalchemy==1.4.29
- flask-wtf==1.0.0, wtforms==3.0.1
- flask-migrate==3.1.0, alembic==1.7.5
- python-dotenv==0.19.2
- pytest==7.1.1, mixer==7.2.2

Целевой Python: **3.10** (greenlet 1.1.2 не собирается на 3.11+).

## Изменения по файлам

### settings.py
- `Config`: `SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')`,
  `SECRET_KEY = os.getenv('SECRET_KEY')`, `SQLALCHEMY_TRACK_MODIFICATIONS = False`.

### fit_track/__init__.py
- Создан `app`, подключены настройки `settings.Config`.
- Создан `db = SQLAlchemy(app)`, `migrate = Migrate(app, db)`.
- В конце файла импорт `models, api_views` (после app/db — против циклов).

### fit_track/models.py
- Модель `WorkoutData(db.Model)`, `__tablename__ = 'workout_data'`.
- Поля: id, date (Date), exercise (String 256), weight (Integer),
  num_circles (Integer), num_reps (Integer), time (Time).

### fit_track/forms.py
- `validate_positive_number`: при `field.data < 0` —
  `ValidationError('Число должно быть положительным')`.
- `WorkoutForm(FlaskForm)`:
  - date: DateField, default = текущая дата, InputRequired.
  - exercise: StringField, InputRequired.
  - weight / num_circles / num_reps: IntegerField,
    InputRequired + validate_positive_number.
  - time: TimeField, default = 00:00:00, format='%H:%M:%S' (БЕЗ required).
  - submit: SubmitField.
- Валидатор именно `InputRequired` (не DataRequired) — чтобы строковый «0»
  из браузера проходил.

### fit_track/api_views.py
- `all_workouts_view` (GET `/`): запрос всех тренировок (сортировка по дате,
  убыв.), список заголовков и вложенный список данных в шаблон index.html.
- `add_workout_view` (GET+POST `/add`): форму строим из form-data (браузер)
  или из JSON через `MultiDict(request.get_json())` (автотесты).
  При валидной форме — сохранение + flash «Тренировка успешно сохранена» +
  redirect; при POST с ошибками — flash «Не удалось сохранить тренировку».
- `page_not_found` (`@app.errorhandler(404)`) → 404.html, код 404.
- `internal_error` (`@app.errorhandler(500)`) → rollback + 500.html, код 500.

### templates/
- base.html: статика через `url_for`, блок `get_flashed_messages`,
  `block content`, `include footer.html`.
- index.html: extends base, ссылка на /add, thead из header, tbody из data.
- add_form.html: extends base, ссылка на главную, форма + csrf_token,
  поля с выводом `field.errors`.
- 404.html: «Упс, ничего не найдено» + `<a href="/">Вернуться на главную</a>`.
- 500.html: «Произошла ошибка на сервере».

### .gitignore
- Добавлены `.venv`, `__pycache__/`, кэши, `.DS_Store`.

## Развёртывание

```bash
uv venv --python 3.10
uv pip install -r requirements.txt
```

## Создание таблицы БД (иначе «no such table: workout_data»)

```bash
uv run flask db init
uv run flask db migrate -m "workout_data"
uv run flask db upgrade
```

## Прогон тестов

```bash
uv run pytest tests/test_config.py
uv run pytest tests/test_database.py
uv run pytest tests/test_endpoints.py::test_get_all
uv run pytest tests/test_endpoints.py -m add
uv run pytest tests/test_endpoints.py -m err
uv run pytest
```

> Предупреждения PytestUnknownMarkWarning про маркеры `add`/`err` —
> ожидаемы (в репозитории нет pytest.ini); на прохождение не влияют.

## Запуск приложения

```bash
uv run flask run --debug
```
