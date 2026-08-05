from json import loads

from server.enums import Status


def test_index(test_client):
    response = test_client.get("/")
    data = response.data.decode()
    json_data = loads(data)

    assert json_data == {"status": Status.OK}


def test_health(test_client):
    response = test_client.get("/")
    data = response.data.decode()
    json_data = loads(data)

    assert json_data == {"status": Status.OK}
