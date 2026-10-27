from mxtw import DIAS, eventos, eventos_del_dia, todos


def test_snapshot_solo_trae_la_edicion_2026():
    assert todos()
    assert all(e.dia in DIAS for e in todos())


def test_eventos_en_orden_cronologico():
    claves = [(e.dia, e.inicio or "") for e in todos()]
    assert claves == sorted(claves)


def test_eventos_del_dia_trae_una_linea_por_evento():
    texto = eventos_del_dia("2026-10-26")
    lineas = texto.splitlines()
    assert lineas[0].startswith("Mexico Tech Week, lunes 26 de octubre:")
    assert len(lineas) == 1 + len(eventos("2026-10-26"))


def test_singular():
    assert "1 evento." in eventos_del_dia("2026-10-25")


def test_dia_sin_eventos_dice_cuales_son_los_dias():
    texto = eventos_del_dia("2026-10-30")
    assert "No hay eventos" in texto
    assert all(d in texto for d in DIAS)


def test_fecha_invalida_no_truena():
    # El LLM puede mandar "martes" en vez de una fecha: debe recibir una pista, no un error
    assert "no es una fecha válida" in eventos_del_dia("martes")


def test_titulos_sin_saltos_de_linea():
    assert all("\n" not in e.titulo and len(e.titulo) <= 140 for e in todos())


def test_lugares_privados_no_exponen_url():
    assert all(not e.lugar.startswith("http") for e in todos())
