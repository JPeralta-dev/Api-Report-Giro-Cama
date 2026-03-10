import pandas as pd

def debug_egresos(df: pd.DataFrame, inicio_mes: str, fin_mes: str, servicio: str | None = None, categoria: str | None = None) -> None:
    ini_mes    = pd.Timestamp(inicio_mes)
    fin_mes_ts = pd.Timestamp(fin_mes)
    
    # ── Filtrar por servicio o categoría si se especifica ─────────────────────
    if servicio:
        df = df[df["SERVICIO"] == servicio].copy()
    if categoria:
        df = df[df["CATEGORIA"] == categoria].copy()
    
    print(f"📋 Registros en tabla: {len(df)}")
    if servicio:   print(f"   🔍 Filtro servicio : {servicio}")
    if categoria:  print(f"   🔍 Filtro categoría: {categoria}")

    # Egresos: FIN dentro del período
    egresos = df[
        (df["FIN"] >= ini_mes) & (df["FIN"] <= fin_mes_ts)
    ].groupby(["IDENTIFICACION", "INGRESO"]).ngroups

    # Días estancia: todos los que tocan el período
    en_periodo = df[
        (df["INICIO"] <= fin_mes_ts) &
        ((df["FIN"] >= ini_mes) | (df["FIN"].isna()))
    ].copy()

    def calc_estancia(row):
        ini = row["INICIO"]
        fin = row["FIN"]
        if ini < ini_mes and pd.notna(fin):
            return (fin - ini_mes).total_seconds() / 86400
        elif pd.isna(fin):
            return (fin_mes_ts - ini).total_seconds() / 86400
        else:
            return (fin - ini).total_seconds() / 86400

    en_periodo["ESTANCIA"] = en_periodo.apply(calc_estancia, axis=1)
    total_dias = en_periodo["ESTANCIA"].sum()

    print(f"\n📊 Resultados:")
    print(f"   Egresos        : {egresos}")
    print(f"   Total días     : {total_dias:.2f}")
    print(f"   Días estancia  : {total_dias/egresos:.2f}" if egresos > 0 else "   Días estancia  : N/A")