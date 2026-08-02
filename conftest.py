import pytest
from flask import Flask

from app.main import app


@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update(
        {
            "TESTING": True,
        }
    )

    yield test_app


@pytest.fixture()
def test_client(test_app: Flask):
    return test_app.test_client()


@pytest.fixture()
def test_runner(test_app: Flask):
    return test_app.test_cli_runner()
