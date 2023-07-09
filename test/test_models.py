import pytest
from mis_criptos.models import Movement, CryptosDAOsqlite
import sqlite3


def test_create_movement():
    m = Movement("0002-01-31", "15:05:25", "EUR", 1000, "BTC", 0.6)
    assert m.date == "0002-01-31"
    assert m.time == "15:05:25"
    assert m.moneda_from == "EUR"
    assert m.cantidad_from == 1000
    assert m.moneda_to == "BTC"
    assert m.cantidad_to == 0.6