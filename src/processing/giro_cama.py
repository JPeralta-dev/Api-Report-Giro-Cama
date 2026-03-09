import pandas as pd
## Variable que indentifica el umbrar de minutos que no pudo haberse cambiado de servicio
##*
# Razon: Se realiza un estudio y muchos medicos por las largas hora de laburo tiende a equivocarse
# de servicio y rapidamente cambian para corregir su error pero esto genera registros incoherente
# lo que se hace es evauluar si es servicio duro menos de 2 minutos entonces es un error#
 
UMBRAL_MINUTOS = 2

SERVICIO_A_CATEGORIA = {
    "UCI": [
        "2DO PISO UNIDAD DE QUEMADOS",
        "3ER PISO UNIDAD CUIDADOS INTENSIVOS CARDIOVASCULAR", ## → UCI Coronaria
        "4TO PISO UNIDAD DE CUIDADOS INTERMEDIOS",
        "5TO PISO A-B UNIDAD DE CUIDADOS INTENSIVOS ADULTOS", ## → UCI Polivalente
        "5TO PISO C-D UNIDAD DE CUIDADOS INTENSIVOS ADULTOS", ## → UCI Polivalente
        "UNIDAD DE CUIDADOS INTENSIVOS ADULTOS (2DO PISO)",
        "UNIDAD DE CUIDADOS INTENSIVOS PEDIATRICOS",
        "UNIDAD DE CUIDADOS INTERMEDIOS ADULTOS (1ER PISO)",
    ],
    "MATERNIDAD": [
        "4TO PISO HOSPITALIZACION MATERNIDAD",
        "4TO PISO UNIDAD DE CUIDADOS INTENSIVO NEONATAL",
        "4TO PISO UCI ALTA DEPENDENCIA OBSTETRICIA",
        "4TO PISO HOSPITALIZACION CUARTO PISO",
    ],
    "HOSPITALIZACION": [
        "2DO PISO HOSPITALIZACION SEGUNDO PISO",
        "2DO PISO ONCOLOGIA VIP 02",
        "3ER PISO HOSPITALIZACION TERCER PISO",
        "5TO PISO HOSPITALIZACION PRESIDENCIAL",
        "5TO PISO HOSPITALIZACION QUINTO PISO",
        "6TO PISO HOSPITALIZACION INFECTOLOGIA SEXTO PISO", 
        "6TO PISO HOSPITALIZACION SEXTO PISO LADO A",
        "6TO PISO HOSPITALIZACION SEXTO PISO LADO B",
        "UNIDAD HEMATO ONCOLOGICA 5 PISO",
    ],
    "PEDIATRIA": [
        "HOSPITALIZACION PEDIATRICA CUARTO PISO",
        "HOSPITALIZACION PEDIATRICA SATELITE",
        "SALA DE OBSERVACION PEDIATRICA",
    ],
    "OTROS": [
        "HOSPITALIZACION SECCION A PISO 1",
        "HOSPITALIZACION SECCION A PISO 2",
        "HOSPITALIZACION SECCION B",
        "HOSPITALIZACION SECCION C",
        "TEMPORALES HOSPITALIZACION",
    ],
}

SERVICIOS_OMITIDOS = [
    "1ER PISO DE REANIMACION. LADO B",
    "1ER PISO OBSERVACION DE URGENCIAS ADULTOS",
    "1ER PISO OBSERVACION DE URGENCIAS TRAUMA",
    "1ER PISO SALA DE PREPARACION QUIRURGICA",
    "1ER PISO SALA DE RECUPERACION",
    "1ER PISO TEMPORAL REMITIDOS",
    "1ER PISO URG.  LADO B EXT",
    "1ER PISO URG. LADO A EXT",
    "HOSPITALIZACION EN CASA",
    "3ER PISO URGENCIAS PLATINO SALA1",
    "3ER PISO URGENCIAS PLATINO SALA2"
]

##UNIR_SERVICIOC = {"4TO PISO TEMPORALES UADO":"4TO PISO UCI ALTA DEPENDENCIA OBSTETRICIA"}

def proccesing_query_giro_cama(df: pd.DataFrame) -> list[dict]:
    print(f"TOTALES REGISTROS EXTRAIDOS: {len(df)}")

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
    # ── 5.0 Renombrar servicios ───────────────────────────────────────────────────    
    RENOMBRAR_SERVICIOS = {
        "4TO PISO TEMPORALES UADO": "4TO PISO UCI ALTA DEPENDENCIA OBSTETRICIA"
    }
    
    df["SERVICIO"] = df["SERVICIO"].replace(RENOMBRAR_SERVICIOS)

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
            es_continuo       = abs((fila_actual["INICIO"] - bloque["FIN"]).total_seconds()) <= 60

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
    df_final["CATEGORIA"] = df_final["SERVICIO"].map(SERVICIO_A_CATEGORIA).fillna("OTROS")

    # print(f"\n📊 Resumen:")
   
    # print(f"   ✅ Registros finales      : {len(df_final)}")
    # print(f"   🏥 Pacientes activos      : {len(activos)}")
    # print(f"   🔴 Fechas inválidas       : {len(invalidos)}")
    # print(f"   ❌ Efímeros eliminados    : {len(efimeros)}")
    # print(f"   🚫 Servicios omitidos     : {len(omitidos)}")
    
    # print(f"\n🔎 Debug colapso:")
    # print(f"   Registros antes de colapsar : {len(df)}")
    # print(f"   Registros después de colapsar: {len(df_completos)}")
    # print(f"   Diferencia (colapsados/perdidos): {len(df) - len(df_completos)}")

    # # Ver si el problema es la igualdad exacta
    # gaps = []
    # for (identificacion, ingreso), grupo in df.groupby(["IDENTIFICACION", "INGRESO"]):
    #     grupo = grupo.sort_values("INICIO").reset_index(drop=True)
    #     for i in range(1, len(grupo)):
    #         diff = (grupo.iloc[i]["INICIO"] - grupo.iloc[i-1]["FIN"]).total_seconds()
    #         if diff != 0:
    #             gaps.append(diff)

    # import numpy as np
    # if gaps:
    #     print(f"\n⏱️ Gaps entre registros consecutivos del mismo paciente:")
    #     print(f"   Gaps con diferencia != 0 : {len(gaps)}")
    #     print(f"   Gap promedio (segundos)  : {np.mean(gaps):.1f}")
    #     print(f"   Gap mínimo               : {min(gaps):.1f}")
    #     print(f"   Gap máximo               : {max(gaps):.1f}")
    
    # # ── DEBUG: Ver nombres reales de servicios ────────────────────────────────────
    # print("\n📋 Servicios únicos en BD:")
    # for servicio in sorted(df["SERVICIO"].unique()):
    #     print(f"   '{servicio}'")
    
    return df_final.to_dict(orient="records")
