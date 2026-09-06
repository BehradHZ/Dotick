import pytest
from django.db import connection
from django.test import Client


def test_liveness_succeeds_without_accessing_the_database():
    response = Client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_readiness_checks_a_real_database():
    response = Client().get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.django_db(transaction=True)
def test_readiness_reports_outage_without_disclosing_connection_details(monkeypatch):
    connection.close()
    with monkeypatch.context() as context:
        context.setitem(connection.settings_dict, "PORT", "1")
        response = Client().get("/ready")
        connection.close()
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}
