# Temas 6 a 9: segmentación, precios, apuntes y guardarails.
D_MENSUAL = 0.008


def churn_maximo_tolerable(margen_nuevo: float, clv_actual: float) -> dict:
    """Churn mensual máximo que puede tener un segmento después de un cambio de precio
    sin que su CLV baje: c' = (m' − CLV × d) ÷ (m' + CLV), con d = 0.008.
    margen_nuevo: margen mensual por cliente con el precio nuevo (US$).
    clv_actual: CLV de hoy del segmento (US$)."""
    if margen_nuevo <= 0 or clv_actual <= 0:
        return {"error": "El margen nuevo y el CLV actual deben ser mayores que 0."}
    arriba = margen_nuevo - clv_actual * D_MENSUAL
    abajo = margen_nuevo + clv_actual
    c = arriba / abajo
    if c < 0:
        return {"error": "Con ese margen nuevo ningún churn mantiene el CLV: "
                         "el margen es menor que CLV × 0.008."}
    return {"churn_maximo": round(c, 4)}


# Pendientes: estimar_elasticidad, proponer_precio, segmentar_clientes, buscar_apunte

HERRAMIENTAS = {
    "churn_maximo_tolerable": churn_maximo_tolerable,
}
