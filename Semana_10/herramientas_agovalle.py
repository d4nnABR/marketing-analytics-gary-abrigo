# Temas 1 a 5: CLV, RFM, churn y uplift, recomendación, CAC.
D_MENSUAL = 0.008


def calcular_clv(margen_mensual: float, churn_mensual: float) -> dict:
    """Calcula el CLV (Customer Lifetime Value, valor de vida del cliente) con la fórmula
    del curso: CLV = m × (1 − c) ÷ (c + d), con d = 0.008 (0.8% mensual).
    margen_mensual: margen por cliente al mes en US$.
    churn_mensual: proporción de clientes que se va cada mes (0.04 = 4%)."""
    if churn_mensual <= 0 or churn_mensual >= 1:
        return {"error": "El churn debe estar entre 0 y 1 (0% y 100%). Si dijeron 4, pregunta si es 4% (0.04)."}
    if margen_mensual <= 0:
        return {"error": "El margen debe ser mayor que 0."}
    m, c, d = margen_mensual, churn_mensual, D_MENSUAL
    return {"clv": round(m * (1 - c) / (c + d), 2)}


def valor_campana_retencion(clientes_contactados: int, uplift: float,
                            clv: float, costo_por_contacto: float) -> dict:
    """Valor esperado de una campaña de retención usando uplift (efecto incremental:
    proporción de contactados que se queda GRACIAS a la campaña, medido contra un grupo de control).
    NUNCA uses la tasa de retención ni el porcentaje que se quedó como uplift: sin grupo de control
    no hay uplift, así que pregunta por la tasa del grupo de control. Si falta el costo por contacto
    o el CLV, pregunta; no los supongas.
    clientes_contactados: número de clientes a contactar.
    uplift: proporción retenida por la campaña (0.05 = 5%).
    clv: valor de vida de un cliente retenido (US$).
    costo_por_contacto: costo de contactar a un cliente (US$)."""
    if uplift < 0 or uplift > 1:
        return {"error": "El uplift debe estar entre 0 y 1. Si dijeron 5, pregunta si es 5% (0.05)."}
    if clientes_contactados <= 0 or clv <= 0 or costo_por_contacto < 0:
        return {"error": "Clientes y CLV deben ser mayores que 0, y el costo no puede ser negativo."}
    retenidos = clientes_contactados * uplift
    valor = retenidos * clv
    costo_total = clientes_contactados * costo_por_contacto
    beneficio = valor - costo_total
    return {"clientes_retenidos_extra": round(retenidos, 1),
            "valor_generado": round(valor, 2),
            "costo_total": round(costo_total, 2),
            "beneficio_neto": round(beneficio, 2),
            "conviene": beneficio > 0,
            "uplift_minimo_para_no_perder": round(costo_por_contacto / clv, 4)}


# Pendientes: metricas_regla_asociacion, relacion_clv_cac

HERRAMIENTAS = {
    "calcular_clv": calcular_clv,
    "valor_campana_retencion": valor_campana_retencion,
}
