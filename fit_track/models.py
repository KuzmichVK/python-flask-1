from fit_track import db


class WorkoutData(db.Model):
    __tablename__ = "workout_data"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    exercise = db.Column(db.String(256))
    weight = db.Column(db.Integer)
    num_circles = db.Column(db.Integer)
    num_reps = db.Column(db.Integer)
    time = db.Column(db.Time)
