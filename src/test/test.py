import pandas as pd
PATH = "C:/Users/juan.peralta/Downloads/data.csv"

def debug_diferencia(python_list):
    powerBI_ingresos = pd.read_csv(PATH)
    powerSet = set(powerBI_ingresos["INGRESO"].to_list())
    print(len(powerBI_ingresos))
    print(len(powerSet))
    python_set = set(python_list)
    faltantes = python_set - powerSet

    print("Ingreso que falta:", faltantes)
    
    

def debug_egresos(
    df: pd.DataFrame,
    inicio_mes: str,
    fin_mes: str,
    servicio: str | None = None,
    categoria: str | None = None
):
    ini_mes = pd.Timestamp(inicio_mes)
    fin_mes_ts = pd.Timestamp(fin_mes)

    df = df.copy()

    # ── Filtros opcionales ─────────────────────────────
    if servicio:
        df = df[df["SERVICIO"] == servicio]

    if categoria:
        df = df[df["CATEGORIA"] == categoria]

    print(f" Registros después de filtro: {len(df)}")

    if servicio:
        print(f" Servicio : {servicio}")

    if categoria:
        print(f" Categoría: {categoria}")

    # ── Registros que tocan el período ─────────────────
    en_periodo = df[
        (df["INICIO"] <= fin_mes_ts) &
        ((df["FIN"] >= ini_mes) | (df["FIN"].isna()))
    ].copy()

    print(f" Registros en periodo: {len(en_periodo)}")

    # ── Egresos reales del periodo ─────────────────────
    egresos_df = en_periodo[
        (en_periodo["FIN"] >= ini_mes) &
        (en_periodo["FIN"] <= fin_mes_ts)
    ].copy()
    print(egresos_df["INGRESO"].tolist())

    debug_diferencia(egresos_df["INGRESO"].tolist())
    egresos = egresos_df.groupby(["IDENTIFICACION","INGRESO"]).ngroups

    # ── Calcular estancia ──────────────────────────────
    def calc_estancia(row):
        ini = max(row["INICIO"], ini_mes)

        if pd.isna(row["FIN"]):
            fin = fin_mes_ts
        else:
            fin = min(row["FIN"], fin_mes_ts)

        return (fin - ini).total_seconds() / 86400

    en_periodo["ESTANCIA"] = en_periodo.apply(calc_estancia, axis=1)

    total_dias = en_periodo["ESTANCIA"].sum()

    print("\n Resultados:")
    print(f"   Egresos        : {egresos}")
    print(f"   Total días     : {total_dias:.2f}")
    print(f"   Días estancia  : {total_dias/egresos:.2f}" if egresos > 0 else "   Días estancia  : N/A")

    # ── DEVOLVER SOLO LOS REGISTROS DEL PERIODO ───────
    return egresos_df["INGRESO"]