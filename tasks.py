from invoke import task


class ENVHelper:
    """Environment variable helper."""

    def with_env(self, cmd: str, env: str) -> str:
        return f"{env} {cmd}"


class DockerHelper:
    """Docker helper."""

    docker_cmd = "docker"

    def up(self, compose_file: str) -> str:
        compose_cmd = "compose"
        up_cmd = "up -d"

        return f"{self.docker_cmd} {compose_cmd} -f {compose_file} {up_cmd}"

    def down(self, compose_file: str) -> str:
        compose_cmd = "compose"
        down_cmd = "down"

        return f"{self.docker_cmd} {compose_cmd} -f {compose_file} {down_cmd}"

    def clear(self) -> str:
        clear_cmd = "system prune --all"

        return f"{self.docker_cmd} {clear_cmd}"


class UVHelper:
    """uv helper."""

    uv_cmd = "uv"

    def run(self, cmd: str) -> str:
        """Run command in virtual environment."""

        run_cmd = "run"

        return f"{self.uv_cmd} {run_cmd} {cmd}"


class SQLAlchemyHelper:
    """SQLAlchemy helper."""

    flask_cmd = "flask"
    db_cmd = "db"

    def migrate(self, app: str, msg: str) -> str:
        """Migrate command."""

        migrate_cmd = f'migrate -m "{msg}"' if msg else "migrate"

        return f"{self.flask_cmd} --app {app} {self.db_cmd} {migrate_cmd}"

    def upgrade(self, app: str) -> str:
        """Upgrade database."""

        upgrade_cmd = "upgrade"

        return f"{self.flask_cmd} --app {app} {self.db_cmd} {upgrade_cmd}"


class PytestHelper:
    """pytest helper."""

    pytest_cmd = "pytest"

    def run(self) -> str:
        return self.pytest_cmd


class RuffHelper:
    """Ruff helper."""

    ruff_cmd = "ruff"

    def check(self, path: str):
        check_cmd = "check --fix"

        return f"{self.ruff_cmd} {check_cmd} {path}"


PROJECT_ROOT = "./"
FLASK_APP = "./server/main.py"
COMPOSE_FILE = "./postgres.compose.yml"

env = ENVHelper()
docker = DockerHelper()
uv = UVHelper()
sqlalchemy = SQLAlchemyHelper()
pytest = PytestHelper()
ruff = RuffHelper()


@task
def up(cmd):
    """Task for container upping."""

    cmd.run(docker.up(COMPOSE_FILE))


@task
def down(cmd):
    """Task for container downing."""

    cmd.run(docker.down(COMPOSE_FILE))


@task
def clear(cmd):
    """Task for Docker cleaning up."""

    cmd.run(docker.clear())


@task
def serve(cmd, debug=False):
    """Task for server starting."""

    if debug:
        cmd.run(env.with_env(cmd=uv.run(FLASK_APP), env="DEBUG=True"))

        return

    cmd.run(uv.run(FLASK_APP))


@task
def migrate(cmd, msg=""):
    """Task for database migrating."""

    cmd.run(uv.run(sqlalchemy.migrate(app=FLASK_APP, msg=msg)))
    cmd.run(uv.run(sqlalchemy.upgrade(FLASK_APP)))


@task
def test(cmd):
    """Task for application testing."""

    cmd.run(uv.run(pytest.run()))


@task
def check(cmd):
    """Task for project linting and formatting."""

    cmd.run(uv.run(ruff.check(PROJECT_ROOT)))
