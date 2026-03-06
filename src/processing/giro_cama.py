import pandas as pd


def proccesing_query_giro_cama(df: pd.DataFrame) -> list[dict]:
    
    print(df)
    # 1. verifico que las fechas esten correctas antes de empezar a procesar
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"] = pd.to_datetime(df["FIN"])
    
    # 2. Ordeno los registros por pacientes, ingreso y fecha de inicio
    df = df.sort_values(["IDENTIFICACION", "INGRESO", "INICIO"]).reset_index(drop=True)
    
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
