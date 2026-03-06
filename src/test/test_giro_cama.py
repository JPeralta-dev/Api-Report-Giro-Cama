# tests/test_giro_cama.py

import pandas as pd
from src.processing.giro_cama import proccesing_query_giro_cama

def test_procesamiento():
    
    data = {
        "SEDE": [
            # JUAN - 123 - INGRESO 1
            "SEDE A", "SEDE A", "SEDE A", "SEDE A", "SEDE A",
            # MARIA - 456 - INGRESO 2
            "SEDE B", "SEDE B", "SEDE B", "SEDE B",
            # CARLOS - 789 - INGRESO 3
            "SEDE A", "SEDE A", "SEDE A", "SEDE A", "SEDE A", "SEDE A",
            # PEDRO - 321 - INGRESO 4 (un solo registro, no hay cambios)
            "SEDE C",
            # LUCIA - 654 - INGRESO 5 (cambia servicio y vuelve al mismo dos veces)
            "SEDE B", "SEDE B", "SEDE B", "SEDE B", "SEDE B", "SEDE B",
        ],
        "IDENTIFICACION": [
            "123", "123", "123", "123", "123",
            "456", "456", "456", "456",
            "789", "789", "789", "789", "789", "789",
            "321",
            "654", "654", "654", "654", "654", "654",
        ],
        "PACIENTE": [
            "JUAN",  "JUAN",  "JUAN",  "JUAN",  "JUAN",
            "MARIA", "MARIA", "MARIA", "MARIA",
            "CARLOS","CARLOS","CARLOS","CARLOS","CARLOS","CARLOS",
            "PEDRO",
            "LUCIA", "LUCIA", "LUCIA", "LUCIA", "LUCIA", "LUCIA",
        ],
        "PLAN_BENEFICIOS": [
            "PLAN1", "PLAN1", "PLAN1", "PLAN1", "PLAN1",
            "PLAN2", "PLAN2", "PLAN2", "PLAN2",
            "PLAN1", "PLAN1", "PLAN1", "PLAN1", "PLAN1", "PLAN1",
            "PLAN3",
            "PLAN2", "PLAN2", "PLAN2", "PLAN2", "PLAN2", "PLAN2",
        ],
        "INGRESO": [
            1, 1, 1, 1, 1,
            2, 2, 2, 2,
            3, 3, 3, 3, 3, 3,
            4,
            5, 5, 5, 5, 5, 5,
        ],
        "CAMA": [
            # JUAN: cambia cama en UCI, luego cirugia, luego vuelve a UCI
            "A101", "A102", "A103", "B201", "A101",
            # MARIA: cambia cama en URGENCIAS, luego pasa a UCI
            "U101", "U102", "C201", "C202",
            # CARLOS: cambia cama varias veces en el mismo servicio
            "P101", "P102", "P103", "P104", "Q201", "P101",
            # PEDRO: un solo registro sin cambios
            "Z101",
            # LUCIA: UCI → CIRUGIA → UCI → CIRUGIA → UCI
            "A101", "A102", "B301", "B302", "A201", "A202",
        ],
        "HSUCODIGO": [
            "U1", "U1", "U1", "C1", "U1",
            "UR1", "UR1", "U1", "U1",
            "P1", "P1", "P1", "P1", "Q1", "P1",
            "Z1",
            "U1", "U1", "C1", "C1", "U1", "U1",
        ],
        "SERVICIO": [
            # JUAN
            "UCI", "UCI", "UCI", "CIRUGIA", "UCI",
            # MARIA
            "URGENCIAS", "URGENCIAS", "UCI", "UCI",
            # CARLOS: PEDIATRIA x4 continuo, luego QUIROFANO, luego vuelve PEDIATRIA
            "PEDIATRIA", "PEDIATRIA", "PEDIATRIA", "PEDIATRIA", "QUIROFANO", "PEDIATRIA",
            # PEDRO
            "URGENCIAS",
            # LUCIA: rebota entre UCI y CIRUGIA
            "UCI", "UCI", "CIRUGIA", "CIRUGIA", "UCI", "UCI",
        ],
        "INICIO": pd.to_datetime([
            # JUAN
            "2026-03-06 08:00", "2026-03-06 10:00", "2026-03-06 14:00",
            "2026-03-06 18:00", "2026-03-06 20:00",
            # MARIA
            "2026-03-05 06:00", "2026-03-05 09:00",
            "2026-03-05 15:00", "2026-03-05 20:00",
            # CARLOS
            "2026-03-04 07:00", "2026-03-04 10:00", "2026-03-04 14:00",
            "2026-03-04 18:00", "2026-03-05 08:00", "2026-03-05 14:00",
            # PEDRO
            "2026-03-06 10:00",
            # LUCIA
            "2026-03-03 08:00", "2026-03-03 12:00",
            "2026-03-03 16:00", "2026-03-03 20:00",
            "2026-03-04 06:00", "2026-03-04 10:00",
        ]),
        "FIN": pd.to_datetime([
            # JUAN
            "2026-03-06 10:00", "2026-03-06 14:00", "2026-03-06 18:00",
            "2026-03-06 20:00", "2026-03-07 08:00",
            # MARIA
            "2026-03-05 09:00", "2026-03-05 15:00",
            "2026-03-05 20:00", "2026-03-06 08:00",
            # CARLOS
            "2026-03-04 10:00", "2026-03-04 14:00", "2026-03-04 18:00",
            "2026-03-05 08:00", "2026-03-05 14:00", "2026-03-05 20:00",
            # PEDRO
            "2026-03-06 18:00",
            # LUCIA
            "2026-03-03 12:00", "2026-03-03 16:00",
            "2026-03-03 20:00", "2026-03-04 06:00",
            "2026-03-04 10:00", "2026-03-04 18:00",
        ]),
        "AINOBSERV": [""] * 22,
    }

    df = pd.DataFrame(data)
    resultado = proccesing_query_giro_cama(df)

    print("\n📋 Resultado del procesamiento:")
    for r in resultado:
        print(
            f"  [{r['IDENTIFICACION']}] {r['PACIENTE']:<8} | "
            f"INGRESO {r['INGRESO']} | "
            f"SERVICIO: {r['SERVICIO']:<12} | "
            f"CAMA: {r['CAMA']:<6} | "
            f"INICIO: {r['INICIO']} → FIN: {r['FIN']}"
        )

    # ─── JUAN ───────────────────────────────────────────────
    juan = [r for r in resultado if r["IDENTIFICACION"] == "123"]
    assert len(juan) == 3,                                      "❌ JUAN: esperaba 3 registros"
    assert juan[0]["SERVICIO"] == "UCI"
    assert juan[0]["CAMA"] == "A101"                            # primera cama
    assert str(juan[0]["INICIO"]) == "2026-03-06 08:00:00"
    assert str(juan[0]["FIN"])    == "2026-03-06 18:00:00"      # colapsa 3 registros
    assert juan[1]["SERVICIO"] == "CIRUGIA"
    assert juan[2]["SERVICIO"] == "UCI"
    assert str(juan[2]["INICIO"]) == "2026-03-06 20:00:00"      # UCI nueva, no se mezcla
    print("\n✅ JUAN correcto")

    # ─── MARIA ──────────────────────────────────────────────
    maria = [r for r in resultado if r["IDENTIFICACION"] == "456"]
    assert len(maria) == 2,                                     "❌ MARIA: esperaba 2 registros"
    assert maria[0]["SERVICIO"] == "URGENCIAS"
    assert maria[0]["CAMA"] == "U101"                           # primera cama
    assert str(maria[0]["INICIO"]) == "2026-03-05 06:00:00"
    assert str(maria[0]["FIN"])    == "2026-03-05 15:00:00"     # colapsa 2 registros
    assert maria[1]["SERVICIO"] == "UCI"
    assert maria[1]["CAMA"] == "C201"
    assert str(maria[1]["FIN"])    == "2026-03-06 08:00:00"     # colapsa 2 registros
    print("✅ MARIA correcto")

    # ─── CARLOS ─────────────────────────────────────────────
    carlos = [r for r in resultado if r["IDENTIFICACION"] == "789"]
    assert len(carlos) == 3,                                    "❌ CARLOS: esperaba 3 registros"
    assert carlos[0]["SERVICIO"] == "PEDIATRIA"
    assert carlos[0]["CAMA"] == "P101"                          # primera cama
    assert str(carlos[0]["INICIO"]) == "2026-03-04 07:00:00"
    assert str(carlos[0]["FIN"])    == "2026-03-05 08:00:00"    # colapsa 4 registros
    assert carlos[1]["SERVICIO"] == "QUIROFANO"
    assert carlos[2]["SERVICIO"] == "PEDIATRIA"                 # vuelve → registro nuevo
    assert str(carlos[2]["INICIO"]) == "2026-03-05 14:00:00"
    print("✅ CARLOS correcto")

    # ─── PEDRO ──────────────────────────────────────────────
    pedro = [r for r in resultado if r["IDENTIFICACION"] == "321"]
    assert len(pedro) == 1,                                     "❌ PEDRO: esperaba 1 registro"
    assert pedro[0]["SERVICIO"] == "URGENCIAS"
    assert pedro[0]["CAMA"] == "Z101"
    assert str(pedro[0]["INICIO"]) == "2026-03-06 10:00:00"
    assert str(pedro[0]["FIN"])    == "2026-03-06 18:00:00"
    print("✅ PEDRO correcto")

    # ─── LUCIA ──────────────────────────────────────────────
    lucia = [r for r in resultado if r["IDENTIFICACION"] == "654"]
    assert len(lucia) == 3,                                     "❌ LUCIA: esperaba 3 registros (UCI-CIRUGIA-UCI)"
    assert lucia[0]["SERVICIO"] == "UCI"
    assert lucia[0]["CAMA"] == "A101"
    assert str(lucia[0]["FIN"])    == "2026-03-03 16:00:00"     # colapsa 2 registros UCI
    assert lucia[1]["SERVICIO"] == "CIRUGIA"
    assert lucia[1]["CAMA"] == "B301"
    assert str(lucia[1]["FIN"])    == "2026-03-04 06:00:00"     # colapsa 2 registros CIRUGIA
    assert lucia[2]["SERVICIO"] == "UCI"
    assert lucia[2]["CAMA"] == "A201"
    assert str(lucia[2]["FIN"])    == "2026-03-04 18:00:00"     # colapsa 2 registros UCI
    print("✅ LUCIA correcto")

    print("\n🎉 Todos los pacientes pasaron correctamente\n")

test_procesamiento()