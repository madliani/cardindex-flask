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


uv = UVHelper()
flask = FlaskHelper()


@task
def run(cmd):
    """Task for server running."""

    app_path = "./app/app.py"

    cmd.run(uv.run(flask.run(app_path)))
