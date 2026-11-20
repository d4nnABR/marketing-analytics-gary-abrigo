# Preguntas por tema. esperado = números que deben aparecer; None = trampa (se revisa a ojo).
BANCO = {
    "CLV": [
        {"pregunta": "Margen US$25 y churn 4% mensual. ¿Cuál es el CLV?", "esperado": [500],
         "herramienta": "calcular_clv"},
        {"pregunta": "Margen US$12 y churn 3% mensual. ¿Cuál es el CLV?", "esperado": [306.32],
         "herramienta": "calcular_clv"},
        {"pregunta": "¿Cuánto vale un cliente si el churn es 4%?", "esperado": None,
         "debe": "Preguntar el margen"},
        {"pregunta": "Margen US$25 y churn de 120%. ¿CLV?", "esperado": None,
         "debe": "Decir que es imposible (churn mayor a 100%)"},
    ],
    "Churn y uplift": [
        {"pregunta": "Contacto a 1,000 clientes, el uplift es 5%, el CLV es US$500 y cada contacto cuesta US$10. "
                     "¿Cuál es el beneficio neto?", "esperado": [15000], "herramienta": "valor_campana_retencion"},
        {"pregunta": "Contacto a 2,000 clientes, uplift 1%, CLV US$300 y costo de US$5 por contacto. ¿Conviene?",
         "esperado": [-4000, 4000], "herramienta": "valor_campana_retencion"},
        {"pregunta": "Contacté a 1,000 clientes y el 30% se quedó. Con CLV de US$500, ¿cuánto ganó la campaña?",
         "esperado": None, "debe": "Explicar que 30% no es uplift y pedir el grupo de control"},
    ],
    "Recomendación": [
        {"pregunta": "Lift de A→B con soportes 0.20, 0.25 y 0.08", "esperado": [1.6],
         "herramienta": "metricas_regla_asociacion"},
    ],
    "CAC": [],
    "Segmentación": [
        {"pregunta": "¿Qué % del gasto concentra el mejor segmento con k-means (k = 3)?", "esperado": [58.9],
         "herramienta": "segmentar_clientes"},
    ],
    "Precios": [
        {"pregunta": "Hoy el CLV es US$500. Si el margen nuevo es US$28 al mes, ¿cuál es el churn máximo que aguanto?",
         "esperado": [4.55, 0.0455], "herramienta": "churn_maximo_tolerable"},
        {"pregunta": "Precio 20, costo 8, elasticidad −1.4 y 1000 unidades. ¿Qué precio propones?",
         "esperado": [22], "herramienta": "proponer_precio"},
    ],
}
