from json import loads

from app.main import Status


def test_index(test_client):
    response = test_client.get("/")

    assert loads(response.data.decode()) == {"status": Status.Ok}


def test_health(test_client):
    response = test_client.get("/")

    assert loads(response.data.decode()) == {"status": Status.Ok}
