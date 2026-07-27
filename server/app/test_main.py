def test_hello_world(test_client):
    response = test_client.get("/")

    assert response.data.decode() == "Hello, World!"
