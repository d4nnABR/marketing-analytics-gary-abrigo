# CLV, RFM y BG/NBD

## CLV (Customer Lifetime Value, valor de vida del cliente)
Fórmula del curso (margen y churn mensuales):
CLV = m × (1 − c) ÷ (c + d)
- m = margen mensual por cliente en US$ (precio − costo por cliente).
- c = churn mensual: proporción de clientes que se va cada mes (4% = 0.04).
- d = tasa de descuento mensual. En el curso d = 0.008 (0.8% mensual).

Ejemplo resuelto: m = US$25, c = 4%, d = 0.8%.
CLV = 25 × (1 − 0.04) ÷ (0.04 + 0.008) = 25 × 0.96 ÷ 0.048 = 24 ÷ 0.048 = US$500.

Vida esperada del cliente = 1 ÷ c. Con c = 4%: 1 ÷ 0.04 = 25 meses.

Las tres palancas del CLV: subir el margen (precio), bajar el churn (retención) y subir el ARPU (Average Revenue Per User, ingreso promedio por usuario) con venta cruzada. El CAC (costo de adquirir un cliente) se compara contra el CLV.

## RFM
RFM = Recencia (días desde la última compra), Frecuencia (número de compras) y Monto (gasto total). Cada cliente recibe un puntaje de 1 a 5 en cada dimensión según su quintil (5 = mejor; en recencia, 5 = compró hace menos días).
- Campeones: R, F y M altos (por ejemplo 5-5-5): premiar y pedir referidos.
- En riesgo: R bajo con F y M altos (compraban mucho y dejaron de venir): campaña de recuperación.
- Nuevos: R alto, F bajo.
- Perdidos: R, F y M bajos: no invertir mucho.

## BG/NBD
Modelo probabilístico (Beta Geométrica / Binomial Negativa) para clientes sin contrato: estima cuántas compras hará un cliente y la probabilidad de que siga "vivo" P(vivo). Usa x (número de compras repetidas), t_x (momento de la última compra) y T (antigüedad del cliente). Un cliente que compraba seguido y lleva mucho tiempo sin comprar tiene P(vivo) baja. Se valida separando un periodo de calibración y uno de prueba (holdout).
