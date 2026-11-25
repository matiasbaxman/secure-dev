import re
import pytest
from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app(tmp_path / "t.db")
    app.config["TESTING"] = True
    return app.test_client()


def token(client, path="/login"):
    html = client.get(path).get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([^"]+)"', html)
    return m.group(1) if m else ""


def login(client, user="ana", pw="ana123"):
    return client.post("/login", data={"username": user, "password": pw, "csrf_token": token(client)})


def test_login_ok(client):
    r = login(client)
    assert r.status_code == 302


def test_sql_injection_en_busqueda(client):
    login(client)
    r = client.get("/search", query_string={"q": "' OR '1'='1"})
    assert "Sin resultados" in r.get_data(as_text=True)


def test_xss_almacenado_en_comentarios(client):
    login(client)
    t = token(client, "/tickets/1")
    client.post("/tickets/1/comments", data={"body": "<script>alert(1)</script>", "csrf_token": t})
    html = client.get("/tickets/1").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html


def test_idor_ticket_ajeno(client):
    login(client)  # ana intenta ver ticket de bruno
    assert client.get("/tickets/2").status_code == 404


def test_idor_comentar_ticket_ajeno(client):
    login(client)
    t = token(client, "/tickets/1")
    assert client.post("/tickets/2/comments", data={"body": "x", "csrf_token": t}).status_code == 404


def test_csrf_login_sin_token(client):
    r = client.post("/login", data={"username": "ana", "password": "ana123"})
    assert r.status_code == 400


def test_cabeceras_de_seguridad(client):
    r = client.get("/login")
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "default-src" in r.headers.get("Content-Security-Policy", "")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
