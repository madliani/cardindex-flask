from invoke import task


class UVHelper:
    """uv helper."""

    uv_cmd = "uv"

    def run(self, cmd: str) -> str:
        """Run command in virtual environment."""

        run_cmd = "run"

        return f"{self.uv_cmd} {run_cmd} {cmd}"


class FlaskHelper:
    """Flask helper."""

    flask_cmd = "flask"

    def serve(self, app_path: str, debug=False) -> str:
        """Run Flask server."""

        run_cmd = "run --debug" if debug else "run"

        return f"{self.flask_cmd} --app {app_path} {run_cmd}"


class SQLAlchemyHelper:
    """SQLAlchemy helper."""

    flask_cmd = "flask"
    db_cmd = "db"

    def migrate(self, app_path: str, msg: str) -> str:
        """Migrate command."""

        migrate_cmd = f'migrate -m "{msg}"' if msg else "migrate"

        return f"{self.flask_cmd} --app {app_path} {self.db_cmd} {migrate_cmd}"

    def upgrade(self, app_path: str) -> str:
        """Upgrade database."""

        upgrade_cmd = "upgrade"

        return f"{self.flask_cmd} --app {app_path} {self.db_cmd} {upgrade_cmd}"


class PytestHelper:
    """pytest helper."""

    pytest_cmd = "pytest"

    def run(self) -> str:
        return self.pytest_cmd


APP_PATH = "./app/main.py"

uv = UVHelper()
flask = FlaskHelper()
sqlalchemy = SQLAlchemyHelper()
pytest = PytestHelper()


@task
def serve(cmd, debug=False):
    """Task for server running."""

    cmd.run(uv.run(flask.serve(app_path=APP_PATH, debug=debug)))


@task
def db(cmd, subcmd, msg=""):
    """Task for database migrating."""

    if subcmd == "migrate":
        cmd.run(uv.run(sqlalchemy.migrate(app_path=APP_PATH, msg=msg)))
        cmd.run(uv.run(sqlalchemy.upgrade(APP_PATH)))

        return


@task
def test(cmd):
    """Task for server testing."""

    cmd.run(uv.run(pytest.run()))
