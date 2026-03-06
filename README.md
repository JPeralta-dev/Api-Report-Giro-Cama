#   IDENTIFICACION | INGRESO | SERVICIO | CAMA  | INICIO              | FIN
    123            | 1       | UCI      | A101  | 06/03/2026 08:00    | 06/03/2026 10:00   ← se elimina
    123            | 1       | UCI      | A102  | 06/03/2026 10:00    | 06/03/2026 14:00   ← se elimina
    123            | 1       | UCI      | A103  | 06/03/2026 14:00    | 06/03/2026 18:00   ← se elimina
    123            | 1       | CIRUGÍA  | B201  | 06/03/2026 18:00    | 06/03/2026 20:00   ← real
    123            | 1       | UCI      | A101  | 06/03/2026 20:00    | 07/03/2026 08:00   ← real (volvió)

# Resultado esperado:
    123            | 1       | UCI      | ---   | 06/03/2026 08:00    | 06/03/2026 18:00   ← colapsado
    123            | 1       | CIRUGÍA  | B201  | 06/03/2026 18:00    | 06/03/2026 20:00   ← intacto
    123            | 1       | UCI      | ---   | 06/03/2026 20:00    | 07/03/2026 08:00   ← intacto (es otra estadía)