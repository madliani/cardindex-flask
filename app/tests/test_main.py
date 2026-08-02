from json import loads

from app.main import Status


def test_index(test_client):
    response = test_client.get("/")
    data = response.data.decode()

    assert loads(data) == {"status": Status.Ok}


def test_health(test_client):
    response = test_client.get("/")
    data = response.data.decode()

    assert loads(data) == {"status": Status.Ok}
