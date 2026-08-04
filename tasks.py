from invoke import task


class ENVHelper:
    """Environment variable helper."""

    def with_env(self, cmd: str, env: str) -> str:
        return f"{env} {cmd}"


class DockerHelper:
    """Docker helper."""

    docker_cmd = "docker"

    def up(self, config_path: str | None = None) -> str:
        compose_cmd = "compose"
        up_cmd = "up -d"

        if config_path is not None:
            return f"{self.docker_cmd} {compose_cmd} -f {config_path} {up_cmd}"

        return f"{self.docker_cmd} {compose_cmd} {up_cmd}"

    def down(self, config_path: str | None = None) -> str:
        compose_cmd = "compose"
        down_cmd = "down"

        if config_path is not None:
            return (
                f"{self.docker_cmd} {compose_cmd} -f {config_path} {down_cmd}"
            )

        return f"{self.docker_cmd} {compose_cmd} {down_cmd}"

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


APP_PATH = "./server/main.py"

env = ENVHelper()
docker = DockerHelper()
uv = UVHelper()
sqlalchemy = SQLAlchemyHelper()
pytest = PytestHelper()


@task
def up(cmd, file=""):
    """Task for container upping."""

    if file:
        cmd.run(docker.up(file))

        return

    cmd.run(docker.up())


@task
def down(cmd, file=""):
    """Task for container downing."""

    if file:
        cmd.run(docker.down(file))

        return

    cmd.run(docker.down())


@task
def clear(cmd):
    """Task for Docker cleaning up."""

    cmd.run(docker.clear())


@task
def serve(cmd, debug=False):
    """Task for server starting."""

    if debug:
        cmd.run(env.with_env(cmd=uv.run(APP_PATH), env="DEBUG=True"))

        return

    cmd.run(uv.run(APP_PATH))


@task
def migrate(cmd, msg=""):
    """Task for database migrating."""

    cmd.run(uv.run(sqlalchemy.migrate(app_path=APP_PATH, msg=msg)))
    cmd.run(uv.run(sqlalchemy.upgrade(APP_PATH)))


@task
def test(cmd):
    """Task for application testing."""

    cmd.run(uv.run(pytest.run()))
