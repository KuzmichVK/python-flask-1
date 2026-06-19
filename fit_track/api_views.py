from flask import flash, redirect, render_template, request, url_for
from werkzeug.datastructures import MultiDict

from fit_track import app, db
from fit_track.forms import WorkoutForm
from fit_track.models import WorkoutData


@app.route("/")
def all_workouts_view():
    """Функция для предоставления всех сохранённых тренировок."""
    workouts = WorkoutData.query.order_by(WorkoutData.date.desc()).all()
    header = [
        "Дата",
        "Упражнение",
        "Вес",
        "Количество кругов",
        "Количество повторов",
        "Время выполнения",
    ]
    data = [
        [w.date, w.exercise, w.weight, w.num_circles, w.num_reps, w.time]
        for w in workouts
    ]
    return render_template("index.html", header=header, data=data)


@app.route("/add", methods=["GET", "POST"])
def add_workout_view():
    """Функция для предоставления и обработки формы WorkoutForm."""
    # Данные могут прийти как form-data (из браузера) или как JSON (автотесты).
    # Во втором случае передаём JSON в форму как formdata через MultiDict.
    if request.method == "POST" and request.is_json:
        form = WorkoutForm(MultiDict(request.get_json()))
    else:
        form = WorkoutForm()
    if form.validate_on_submit():
        workout = WorkoutData(
            date=form.date.data,
            exercise=form.exercise.data,
            weight=form.weight.data,
            num_circles=form.num_circles.data,
            num_reps=form.num_reps.data,
            time=form.time.data,
        )
        db.session.add(workout)
        db.session.commit()
        flash("Тренировка успешно сохранена")
        return redirect(url_for("all_workouts_view"))
    if request.method == "POST":
        flash("Не удалось сохранить тренировку")
    return render_template("add_form.html", form=form)


@app.errorhandler(404)
def page_not_found(error):
    """Функция для обработки 404 ошибки."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Функция для обработки 500 ошибки."""
    db.session.rollback()
    return render_template("500.html"), 500
