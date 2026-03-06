import pandas as pd

## Variable que indentifica el umbrar de minutos que no pudo haberse cambiado de servicio
##*
# Razon: Se realiza un estudio y muchos medicos por las largas hora de laburo tiende a equivocarse
# de servicio y rapidamente cambian para corregir su error pero esto genera registros incoherente
# lo que se hace es evauluar si es servicio duro menos de 2 minutos entonces es un error#
UMBRAL_MINUTOS = 2

SERVICIO_OMITIDOS = ["1ER PISO DE REANIMACION. LADO B",
                     "1ER PISO OBSERVACION DE URGENCIAS ADULTOS",
                     "1ER PISO OBSERVACION DE URGENCIAS TRAUMA",
                     "1ER PISO SALA DE PREPARACION QUIRURGICA",
                     "1ER PISO SALA DE RECUPERACION",
                     "1ER PISO TEMPORAL REMITIDOS",
                     "1ER PISO URG.  LADO B EXT",
                     "1ER PISO URG. LADO A EXT",
                     "HOSPITALIZACION EN CASA"
                     ]

import pandas as pd

UMBRAL_MINUTOS = 2

SERVICIOS_OMITIDOS = [
    "1ER PISO DE REANIMACION. LADO B",
    "1ER PISO OBSERVACION DE URGENCIAS ADULTOS",
    "1ER PISO OBSERVACION DE URGENCIAS TRAUMA",
    "1ER PISO SALA DE PREPARACION QUIRURGICA",
    "1ER PISO SALA DE RECUPERACION",
    "1ER PISO TEMPORAL REMITIDOS",
    "1ER PISO URG.  LADO B EXT",
    "1ER PISO URG. LADO A EXT",
    "HOSPITALIZACION EN CASA"
]

def proccesing_query_giro_cama(df: pd.DataFrame) -> list[dict]:

    # ── 1. Tipos de fecha ─────────────────────────────────────────────────────
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"]    = pd.to_datetime(df["FIN"])

    # ── 2. Separar activos (sin FIN) ──────────────────────────────────────────
    activos = df[df["FIN"].isna()].copy()
    df      = df[df["FIN"].notna()].reset_index(drop=True)

    # ── 3. Descartar fechas inválidas (FIN < INICIO) ──────────────────────────
    df["DURACION_MIN"] = (df["FIN"] - df["INICIO"]).dt.total_seconds() / 60
    invalidos = df[df["DURACION_MIN"] < 0].copy()
    df        = df[df["DURACION_MIN"] >= 0].reset_index(drop=True)

    # ── 4. Descartar efímeros (error médico < UMBRAL_MINUTOS) ─────────────────
    efimeros = df[df["DURACION_MIN"] < UMBRAL_MINUTOS].copy()
    df       = df[df["DURACION_MIN"] >= UMBRAL_MINUTOS].reset_index(drop=True)

    # ── 5. Omitir servicios excluidos ─────────────────────────────────────────
    omitidos = df[df["SERVICIO"].isin(SERVICIOS_OMITIDOS)].copy()
    df       = df[~df["SERVICIO"].isin(SERVICIOS_OMITIDOS)].reset_index(drop=True)

    # ── 6. Ordenar ────────────────────────────────────────────────────────────
    df = df.sort_values(["IDENTIFICACION", "INGRESO", "INICIO"]).reset_index(drop=True)

    # ── 7. Colapsar cambios de cama en mismo servicio continuo ────────────────
    resultado = []

    for (identificacion, ingreso), grupo in df.groupby(["IDENTIFICACION", "INGRESO"]):
        grupo  = grupo.reset_index(drop=True)
        bloque = grupo.iloc[0].to_dict()

        for i in range(1, len(grupo)):
            fila_actual       = grupo.iloc[i]
            es_mismo_servicio = fila_actual["SERVICIO"] == bloque["SERVICIO"]
            es_continuo       = fila_actual["INICIO"]   == bloque["FIN"]

            if es_mismo_servicio and es_continuo:
                bloque["FIN"] = fila_actual["FIN"]
            else:
                resultado.append(bloque)
                bloque = fila_actual.to_dict()

        resultado.append(bloque)

    # ── 8. Construir DataFrame final ──────────────────────────────────────────
    columnas = ["SEDE", "IDENTIFICACION", "PACIENTE", "PLAN_BENEFICIOS",
                "INGRESO", "CAMA", "SERVICIO", "INICIO", "FIN", "AINOBSERV"]

    df_completos = pd.DataFrame(resultado)[columnas] if resultado else pd.DataFrame(columns=columnas)
    df_activos   = activos[columnas]
    df_final     = pd.concat([df_completos, df_activos], ignore_index=True)
    df_final     = df_final.sort_values(["IDENTIFICACION", "INGRESO", "INICIO"]).reset_index(drop=True)

    df_final["FIN"] = df_final["FIN"].astype(object).where(df_final["FIN"].notna(), other=None)

    print(f"\n📊 Resumen:")
    print(f"   ✅ Registros finales      : {len(df_final)}")
    print(f"   🏥 Pacientes activos      : {len(activos)}")
    print(f"   🔴 Fechas inválidas       : {len(invalidos)}")
    print(f"   ❌ Efímeros eliminados    : {len(efimeros)}")
    print(f"   🚫 Servicios omitidos     : {len(omitidos)}")

    return df_final.to_dict(orient="records")
