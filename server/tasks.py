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

    def run(self, app_path: str) -> str:
        """Run Flask server."""

        run_cmd = "run"

        return f"{self.flask_cmd} --app {app_path} {run_cmd}"


class SQLAlchemyHelper:
    """SQLAlchemy helper."""

    flask_cmd = "flask"
    db_cmd = "db"

    def init(self, app_path: str) -> str:
        """Initialize database."""

        init_cmd = "init"

        return f"{self.flask_cmd} --app {app_path} {self.db_cmd} {init_cmd}"

    def migrate(self, app_path: str, msg: str) -> str:
        """Migrate command."""

        migrate_cmd = "migrate"

        return f'{self.flask_cmd} --app {app_path} {self.db_cmd} {migrate_cmd} -m "{msg}"'

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
def serve(cmd):
    """Task for server running."""

    cmd.run(uv.run(flask.run(APP_PATH)))


@task
def db(cmd, subcmd, msg=""):
    """Task for database initializing."""

    if subcmd == "init":
        cmd.run(uv.run(sqlalchemy.init(APP_PATH)))

        return

    if subcmd == "migrate":
        cmd.run(uv.run(sqlalchemy.migrate(APP_PATH, msg)))

        return


@task
def test(cmd):
    """Task for server testing."""

    cmd.run(uv.run(pytest.run()))
