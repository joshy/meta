from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TaskInfo(db.Model):
    __tablename__ = 'task_info'

    id = db.Column(db.Integer, primary_key=True)

    dir_name = db.Column(db.String)
    patient_id = db.Column(db.String)
    accession_number = db.Column(db.String)
    series_number = db.Column(db.String)

    study_id = db.Column(db.String)

    creation_time = db.Column(db.DateTime, default=datetime.now())
    execution_time = db.Column(db.DateTime, default=datetime.now())  # TODO: Not sure if this is used
    started = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    running_time = db.Column(db.Interval)
    flag_finished = db.Column(db.Boolean, index=True)
    exception = db.Column(db.String)
    command = db.Column(db.String)
    status = db.Column(db.String)
    task_type = db.Column(db.String, index=True)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return (
            '<TaskInfo ' +
            ', '.join(
                ['{0!r}: {1!r}'.format(*x) for x in self.__dict__.items()]) +
            '>'
        )
