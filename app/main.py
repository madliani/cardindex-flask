from enum import StrEnum

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cardindex.db"


class BaseModel(DeclarativeBase):
    pass


db = SQLAlchemy(app=app, metadata=BaseModel.metadata, model_class=BaseModel)
migrate = Migrate(app=app, db=db)


# ty:ignore[unsupported-base]
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    desc: Mapped[str] = mapped_column(unique=False, nullable=False)


class Status(StrEnum):
    Error = "error"
    Ok = "ok"


@app.route("/")
def index():
    return {"status": Status.Ok}


@app.route("/health")
def health():
    return {"status": Status.Ok}
