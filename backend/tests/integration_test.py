import requests

shorted_url: str = ""

class TestRouters:
    session = requests.Session()

    cookies: str = ""


    def test_account_register(self):
        payload = {"username": "admins2", "password": "admins2"}

        resp = self.session.post("http://0.0.0.0:8000/register", json=payload)

        assert resp.status_code == 200

    def test_account_login(self):
        payload = {"username": "admins2", "password": "admins2"}

        resp = self.session.post("http://0.0.0.0:8000/login", json=payload)

        assert resp.status_code == 200

        assert resp.cookies.get_dict()["session"] != None

    def test_create_link(self):
        payload = {"url": "https://www.google.com", "time_ending": "7d"}

        resp = self.session.post(
            "http://0.0.0.0:8000/create_link",
            json=payload
        )

        assert resp.status_code == 200

        assert "http://0.0.0.0:8000/" in resp.json()["url"]

        global shorted_url
        shorted_url = resp.json()["url"]

    def test_get_link(self):
        global shorted_url

        resp = self.session.get(shorted_url)
        assert resp.status_code == 200

    def test_delete_link(self):
        global shorted_url

        resp = self.session.delete(shorted_url)
        assert resp.status_code == 200
