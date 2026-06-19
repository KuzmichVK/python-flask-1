# Определите здесь объект приложения Flask
# Подключите настройки, статику
# Определите объект базы данных, миграции
# Импортируйте файл с view-функциями

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("settings.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Импорт в конце файла — после создания app и db, чтобы избежать
# циклических импортов. Модули регистрируют модель, маршруты и
# обработчики ошибок (ради побочного эффекта).
from fit_track import api_views, models  # noqa: E402,F401
