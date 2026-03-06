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

def proccesing_query_giro_cama(df: pd.DataFrame) -> list[dict]:
    
    print(df)
    # 1. verifico que las fechas esten correctas antes de empezar a procesar
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"] = pd.to_datetime(df["FIN"])
    
    # 2. Ordeno los registros por pacientes, ingreso y fecha de inicio
    df = df.sort_values(["IDENTIFICACION", "INGRESO", "INICIO"]).reset_index(drop=True)
    
    # # ── 1. Eliminar registros efímeros ────────────────────────────────────────
    # df["DURACION_MIN"] = (df["FIN"] - df["INICIO"]).dt.total_seconds() / 60
    # efimeros = df[df["DURACION_MIN"] < UMBRAL_MINUTOS].copy()
    # df = df[df["DURACION_MIN"] >= UMBRAL_MINUTOS].reset_index(drop=True)

    # total_eliminados = len(efimeros)
    # print(total_eliminados)
    # if total_eliminados > 0:
    #     print(f"\n🗑️  Registros efímeros eliminados (< {UMBRAL_MINUTOS} min): {total_eliminados}")
    #     for _, row in efimeros.iterrows():
    #         duracion_seg = (row["FIN"] - row["INICIO"]).total_seconds()
    #         print(
    #             f"   ❌ [{row['IDENTIFICACION']}] {row['PACIENTE']} | "
    #             f"INGRESO {row['INGRESO']} | "
    #             f"SERVICIO: {row['SERVICIO']} | "
    #             f"CAMA: {row['CAMA']} | "
    #             f"DURACIÓN: {duracion_seg:.0f} seg | "
    #             f"{row['INICIO']} → {row['FIN']}"
    #         )
    # else:
    #     print(f"\n✅ No se encontraron registros efímeros")
    
    
    resultado = []
    
    
    # 3. Agrupar por paciente e ingreso
    for (identificacion, ingreso), grupo in df.groupby(["IDENTIFICACION", "INGRESO"]):
        grupo = grupo.reset_index(drop=True)

        # Tomar el primer registro como base del bloque actual
        bloque = grupo.iloc[0].to_dict()

        for i in range(1, len(grupo)):
            fila_actual = grupo.iloc[i]

            es_mismo_servicio = fila_actual["SERVICIO"] == bloque["SERVICIO"]
            es_continuo = fila_actual["INICIO"] == bloque["FIN"]  # el inicio nuevo == fin anterior

            if es_mismo_servicio and es_continuo:
                # Mismo servicio continuo → extender el FIN, mantener todo lo demás
                bloque["FIN"] = fila_actual["FIN"]
            else:
                # Cambio real de servicio → guardar bloque anterior y abrir uno nuevo
                resultado.append(bloque)
                bloque = fila_actual.to_dict()

        # Guardar el último bloque del ingreso
        resultado.append(bloque)
    df_final = pd.DataFrame(resultado)

    # 5. Columnas a retornar (sin HSUCODIGO que es código interno)
    columnas = ["SEDE", "IDENTIFICACION", "PACIENTE", "PLAN_BENEFICIOS",
                "INGRESO", "CAMA", "SERVICIO", "INICIO", "FIN", "AINOBSERV"]

    df_final = df_final[columnas]
    print(df_final)
    return df_final.to_dict(orient="records")
