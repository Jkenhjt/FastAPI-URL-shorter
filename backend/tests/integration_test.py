import requests

username: str = "admins2"
password: str = "admins2"

cookies: str = ""

org_url: str = "https://www.google.com"
shorted_url: str = ""

def test_account_register():
    payload = {
        "username": username,
        "password": password
    }

    resp = requests.post("http://0.0.0.0:8000/register",
                         json=payload)

    assert resp.status_code == 200

def test_account_login():
    payload = {
        "username": username,
        "password": password
    }

    resp = requests.post("http://0.0.0.0:8000/login",
                         json=payload)

    assert resp.status_code == 200

    assert resp.cookies.get_dict()["session"] != None

    global cookies
    cookies = resp.cookies.get_dict()["session"]

def test_create_link():
    payload = {
        "url": org_url,
        "time_ending": "7d"
    }

    resp = requests.post("http://0.0.0.0:8000/create_link",
                         json=payload,
                         cookies={"session": cookies})

    assert resp.status_code == 200

    assert "http://0.0.0.0:8000/" in resp.json()["url"]

    global shorted_url
    shorted_url = resp.json()["url"]

def test_get_link():
    resp = requests.get(shorted_url)
    assert resp.status_code == 200

def test_delete_link():
    resp = requests.delete(shorted_url,
                           cookies={"session": cookies})
    assert resp.status_code == 200