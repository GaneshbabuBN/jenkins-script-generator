from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScriptHistory(db.Model):
    __tablename__ = "script_history"

    id = db.Column(db.Integer, primary_key=True)

    project_name = db.Column(
        db.String(200),
        nullable=False
    )

    github_url = db.Column(
        db.Text,
        nullable=False
    )

    generated_script = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )