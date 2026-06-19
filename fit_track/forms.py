import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    StringField,
    SubmitField,
    TimeField,
)
from wtforms.validators import InputRequired, ValidationError


def validate_positive_number(form, field):
    # Валидатор положительных чисел. Значение берём из field.data.
    # При отрицательном значении — поднимаем ValidationError с сообщением.
    if field.data is not None and field.data < 0:
        raise ValidationError("Число должно быть положительным")


class WorkoutForm(FlaskForm):
    date = DateField(
        "Дата тренировки",
        default=datetime.date.today,
        validators=[InputRequired(message="Обязательное поле")],
    )
    exercise = StringField(
        "Описание упражнения",
        validators=[InputRequired(message="Обязательное поле")],
    )
    weight = IntegerField(
        "Используемый вес",
        validators=[
            InputRequired(message="Обязательное поле"),
            validate_positive_number,
        ],
    )
    num_circles = IntegerField(
        "Количество кругов",
        validators=[
            InputRequired(message="Обязательное поле"),
            validate_positive_number,
        ],
    )
    num_reps = IntegerField(
        "Количество повторений",
        validators=[
            InputRequired(message="Обязательное поле"),
            validate_positive_number,
        ],
    )
    time = TimeField(
        "Время выполнения упражнения",
        default=datetime.time(0, 0, 0),
        format=["%H:%M:%S", "%H:%M"],
    )
    submit = SubmitField("Добавить")
