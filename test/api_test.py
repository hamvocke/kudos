from helloworld import app

app = app.app.test_client()


def test_should_return_200_status():
    response = app.get("/helloworld")
    assert response.status_code == 200


def test_should_return_hello_world_body():
    response = app.get("/helloworld")
    assert b"Hello World!" in response.data
