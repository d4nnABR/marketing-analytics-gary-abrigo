# Churn, retención y uplift

## Churn
Churn = clientes que se van en el periodo ÷ clientes al inicio del periodo. Retención = 1 − churn.
Un modelo de churn predice QUIÉN se va a ir (probabilidad). No dice a quién conviene contactar.

## Uplift (efecto incremental)
Uplift = tasa de retención del grupo contactado − tasa de retención del grupo de control (no contactado).
Solo un experimento (prueba A/B con grupo de control) mide el uplift real.

Cuatro tipos de clientes:
- Persuadibles: se quedan solo si los contactas. Son el objetivo.
- Seguros (sure things): se quedan igual. Contactarlos es gastar de más.
- Perdidos (lost causes): se van igual.
- No molestar (sleeping dogs): la campaña los empuja a irse.

Modelos: T-learner (un modelo para tratados y otro para control; uplift = diferencia de predicciones). Se evalúa con la curva Qini: cuánto uplift acumulado se gana al contactar primero a los de mayor uplift predicho.

## Valor de una campaña de retención
Clientes retenidos extra = clientes contactados × uplift.
Beneficio neto = retenidos extra × CLV − clientes contactados × costo por contacto.
Uplift mínimo para no perder dinero = costo por contacto ÷ CLV.

Ejemplo resuelto: 2,000 clientes, uplift 4%, CLV US$500, costo US$8 por contacto.
Retenidos extra = 2,000 × 0.04 = 80. Valor = 80 × 500 = US$40,000. Costo = 2,000 × 8 = US$16,000.
Beneficio neto = 40,000 − 16,000 = US$24,000. Uplift mínimo = 8 ÷ 500 = 1.6%.
