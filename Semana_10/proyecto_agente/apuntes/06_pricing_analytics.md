# Pricing analytics

## Elasticidad precio
ε = % de cambio en unidades ÷ % de cambio en precio. ε < −1: elástica (sensible al precio); entre −1 y 0: inelástica.
- Cuenta rápida con dos puntos: %ΔQ ÷ %ΔP. Precio 50 → 55 (+10%), unidades 1,000 → 880 (−12%): ε = −12 ÷ 10 = −1.2.
- Con logaritmos (lo que usa la regresión ln(unidades) contra ln(precio)): ε = ln(880/1,000) ÷ ln(55/50) = ln(0.88) ÷ ln(1.10) = −1.34. Las dos cuentas difieren porque los porcentajes simples dependen de la base y de la dirección del cambio; con varios precios se usa la regresión ln-ln y su pendiente es ε.

## Precio óptimo
Si ε < −1: P* = C × ε ÷ (1 + ε), donde C = costo por unidad o por cliente.
Ejemplo: C = US$30, ε = −2 → P* = 30 × (−2) ÷ (−1) = US$60.
Unidades a un precio p: Q(p) = Q0 × (p ÷ p0)^ε. Utilidad = (p − C) × Q(p).
Ejemplo con p0 = 50, Q0 = 1,000, C = 30, ε = −2: utilidad hoy = 20 × 1,000 = 20,000; a 55: (25) × 1,000 × (55/50)^(−2) = 20,661; a 60: 20,833.

## Reglas típicas (restricciones)
Cambio máximo ±10% por ciclo; precio ≥ 1.2 × C; si el cambio supera 5%, aprobación humana. Con la regla de ±10%, si P* está lejos se sube por etapas.

## Precio y churn: churn máximo tolerable
c' = (m' − CLV × d) ÷ (m' + CLV), con m' = margen nuevo y CLV = CLV de hoy.
Ejemplo: precio 50, costo 30 (m = 20), churn 5%: CLV = 20 × 0.95 ÷ 0.058 = 327.59. Si el margen sube a 22: c' = (22 − 327.59 × 0.008) ÷ (22 + 327.59) = 19.38 ÷ 349.59 = 5.54%. Si el churn nuevo supera 5.54%, el aumento destruye valor.
Churn nuevo estimado = c × (1 + ε(c) × %ΔP), donde ε(c) es la elasticidad del churn al precio.

## Elasticidad cruzada
εx > 0: sustitutos (si sube el precio de un plan, parte de sus clientes se pasa al otro). Hay que mirar la utilidad de los dos planes juntos.

## Discriminación de precios y paquetes
Precios por segmento según disposición a pagar (WTP, willingness to pay), paquetes (bundles) y promociones. Ojo con la percepción de injusticia de los precios dinámicos.
