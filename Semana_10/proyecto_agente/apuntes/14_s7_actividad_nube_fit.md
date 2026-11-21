# Semana 7 · Actividad Nube Fit: ¿subimos el precio?

Marketing Analytics

Actividad – Nube Fit: ¿subimos el precio?

Modalidad – Grupos de trabajo. La entrega es una hoja de una página por grupo.

Pregunta guía: ¿subimos el precio de cada segmento y qué le recomendamos a la dirección?

## Símbolos (todos se usan en este caso)

| Símbolo | Qué significa |
| P | Precio de hoy |
| P* | Precio óptimo (el que deja más utilidad) |
| C | Costo por cliente |
| Q | Unidades que se venden al mes |
| ε | Elasticidad: cuántos % cambian las ventas por cada 1% que cambia el precio |
| εx | Elasticidad cruzada: cuántos % cambian las unidades del OTRO segmento por cada 1% que sube el precio de este. Positiva = sustitutos (parte de los clientes se pasa al otro plan) |
| ln | Logaritmo natural (convierte los cambios en porcentajes) |
| m | Margen mensual por cliente = P − C |
| c | Churn mensual: % de clientes que se va cada mes |
| ε(c) | Elasticidad del churn: cuántos % sube el churn por cada 1% que sube el precio |
| d | Tasa de descuento mensual: un dólar futuro vale menos que uno de hoy (0.8%) |
| CLV | Customer lifetime value: valor total que deja un cliente = m × (1 − c) ÷ (c + d) |
| c' | Churn máximo tolerable: el churn al que el CLV queda igual que hoy |

## 1 · El caso

Nube Fit es una empresa ficticia con una app de entrenamiento. Tiene dos segmentos de clientes y la dirección quiere saber si conviene subir el precio de cada uno. Los datos son inventados.

| Segmento | Precio hoy P | Costo C | Unidades al mes Q | Elasticidad ε | Churn mensual c | Elasticidad cruzada εx |
| 1. Constantes | $20 | $8 | 1,000 | Estimar (parte 2) | 3% | +0.5 |
| 2. Casuales | $12 | $8 | 2,000 | Estimar (parte 2) | 6% | +0.2 |

εx de Constantes = +0.5 significa: si el precio de Constantes sube 10%, las unidades de Casuales suben 5%. εx de Casuales = +0.2 significa: si el precio de Casuales sube 10%, las unidades de Constantes suben 2%.

Reglas de la empresa:

El precio no puede cambiar más de 10% por ciclo (tope de ±10%).

El precio nunca puede quedar por debajo de 1.2 × C (margen mínimo).

Si el cambio de precio supera 5%, necesita aprobación humana.

Pregunta 1. Antes de calcular: ¿en cuál segmento esperan que subir el precio sea más riesgoso? Anoten por qué.

| Respuesta del grupo: |

## 2 · Estimar la elasticidad

Abran el notebook Nube_Fit_alumnos.ipynb. La dirección no nos da la elasticidad ε: hay que calcularla con las pruebas de precio anteriores. Corran estas celdas en orden.

Celda 1. Los datos del caso

| import numpy as np, pandas as pd D = 0.008 # d = tasa de descuento mensual (0.8%) datos = pd.DataFrame({ 'segmento': ['Constantes', 'Casuales'], 'precio': [20, 12], # P = precio de hoy 'costo': [8, 8], # C = costo por cliente 'unidades': [1000, 2000], # Q = unidades al mes hoy 'eps_x': [0.5, 0.2], # εx = efecto de SU precio en las unidades del OTRO segmento 'churn': [0.03, 0.06], # c = churn mensual}).set_index('segmento')datos |

Celda 2. Las pruebas de precio anteriores

| # Pruebas de precio anteriores: a cada precio, cuántas unidades se vendieron al mespruebas = pd.DataFrame({ 'segmento': ['Constantes'] * 5 + ['Casuales'] * 5, 'precio': [18, 19, 20, 21, 22, 10.8, 11.4, 12, 12.6, 13.2], 'unidades': [1159, 1074, 1000, 934, 875, 2603, 2274, 2000, 1770, 1576],})pruebas |

Celda 3. Ejemplo resuelto: elasticidad de Constantes

| # EJEMPLO resuelto: elasticidad de Constantesg = pruebas[pruebas.segmento == 'Constantes'] # Pendiente de la recta ln(unidades) contra ln(precio): es la elasticidad ε (como en el Demo 1)eps_const = np.polyfit(np.log(g.precio), np.log(g.unidades), 1)[0]print(f'Elasticidad de Constantes: {eps_const:.2f}') |

Debe imprimir: Elasticidad de Constantes: -1.40.

Celda 4. Su turno: elasticidad de Casuales

| # TU TURNO: elasticidad de Casualesg = pruebas[pruebas.segmento == 'Casuales'] # TU CÓDIGO AQUÍ (calculen eps_casu con la misma fórmula y escríbanla con print) datos['eps'] = [round(eps_const, 1), round(eps_casu, 1)] # ε de cada segmento, a un decimaldatos |

Pregunta 2. ¿Cuánto vale ε en cada segmento y cuál es más sensible al precio? Después, un detalle: con solo dos precios de Constantes ($20 y $22) la cuenta rápida %ΔQ ÷ %ΔP da −1.25. ¿Por qué no coincide con la regresión?

| Respuesta del grupo: |

## 3 · Precio óptimo y restricciones (10 min)

Con ε ya calculada, usen las funciones del Demo 2 de Ritmo para encontrar el precio que deja más utilidad respetando las reglas de la empresa.

Celda 5. Las funciones (no hay que cambiarlas)

| # Las mismas funciones del Demo 2 de Ritmo (no hay que cambiarlas)def precio_optimo(C, eps): return C * eps / (1 + eps) # P* = C × ε ÷ (1 + ε) def aplicar_reglas(p_hoy, p_opt, C): p = min(p_opt, p_hoy * 1.10) # tope: sube máximo 10% p = max(p, p_hoy * 0.90) # tope: baja máximo 10% p = max(p, 1.2 * C) # margen mínimo: precio ≥ 1.2 × C return p def utilidad(p, p_hoy, C, Q, eps): unidades = Q * (p / p_hoy) ** eps # cuántas unidades se venden a p return (p - C) * unidades # utilidad = (p − C) × unidades def clv(m, c, d=D): return m * (1 - c) / (c + d) # CLV = m × (1 − c) ÷ (c + d) def churn_maximo(m_nuevo, clv_hoy, d=D): return (m_nuevo - clv_hoy * d) / (m_nuevo + clv_hoy) # c' |

Celda 6. Ejemplo resuelto: precio de Constantes

| # EJEMPLO resuelto: segmento Constantess = datos.loc['Constantes'] p_opt = precio_optimo(s.costo, s.eps)p_prop = aplicar_reglas(s.precio, p_opt, s.costo) print(f'Precio óptimo P*: ${p_opt:.2f}')print(f'Precio propuesto (reglas): ${p_prop:.2f}')print(f'Utilidad hoy: {utilidad(s.precio, s.precio, s.costo, s.unidades, s.eps):,.0f}')print(f'Utilidad propuesta:{utilidad(p_prop, s.precio, s.costo, s.unidades, s.eps):,.0f}') |

Debe imprimir: P* = $28.00, precio propuesto = $22.00, utilidad hoy = 12,000 y utilidad propuesta = 12,251.

Pregunta 3. P* es $28, pero la propuesta es $22. ¿Por qué no se propone $28? ¿Cuánta utilidad cuesta esa restricción? (Pista: calculen la utilidad en P* con la misma función.)

| Respuesta del grupo: |

Celda 7. Su turno: precio de Casuales

| # TU TURNO: repitan lo mismo para el segmento Casualess = datos.loc['Casuales'] # TU CÓDIGO AQUÍ (calculen p_opt y p_prop) # TU CÓDIGO AQUÍ (impriman P*, precio propuesto y utilidad hoy vs. propuesta) |

Pregunta 4. ¿Qué precio proponen para Casuales y cuánto sube la utilidad? ¿Por qué aquí la restricción casi no cuesta?

| Respuesta del grupo: |

## 4 · Efecto cruzado entre segmentos (10 min)

Constantes y Casuales son dos planes de la misma app. Cuando sube el precio de uno, parte de sus clientes puede pasarse al otro. Eso es lo que mide la elasticidad cruzada εx de la tabla del caso. Hasta ahora calculamos cada segmento por separado; ahora miramos los dos juntos.

Celda 8. La función nueva y un ejemplo resuelto (sube solo Constantes)

| # La función nueva: utilidad de los DOS segmentos juntos, con elasticidad cruzadadef utilidad_total(p_const, p_casu): a, b = datos.loc['Constantes'], datos.loc['Casuales'] q_const = a.unidades * (p_const / a.precio) ** a.eps * (p_casu / b.precio) ** b.eps_x q_casu = b.unidades * (p_casu / b.precio) ** b.eps * (p_const / a.precio) ** a.eps_x u_const = (p_const - a.costo) * q_const u_casu = (p_casu - b.costo) * q_casu return u_const, u_casu # EJEMPLO resuelto: sube SOLO Constantes a $22 (Casuales se queda en $12)hoy = utilidad_total(20, 12)sube = utilidad_total(22, 12)print(f'Constantes: {hoy[0]:,.0f} -> {sube[0]:,.0f}')print(f'Casuales: {hoy[1]:,.0f} -> {sube[1]:,.0f}')print(f'Total: {sum(hoy):,.0f} -> {sum(sube):,.0f}') |

Debe imprimir: Constantes 12,000 → 12,251; Casuales 8,000 → 8,390; total 20,000 → 20,642.

Pregunta 5. Constantes solo subió su propio precio, pero la utilidad de Casuales también cambió. ¿Cuánto ganó cada segmento y qué parte de la ganancia total viene de Casuales?

| Respuesta del grupo: |

Celda 9. Su turno: suben los dos segmentos

| # TU TURNO: suben LOS DOS segmentos (Constantes a $22 y Casuales a $13.20)# TU CÓDIGO AQUÍ (calculen utilidad_total(22, 13.2) e impriman la utilidad de cada segmento y el total) # TU CÓDIGO AQUÍ (comparen con la suma de las dos utilidades propuestas de las celdas 3 y 4: 12,251 + 8,195 = 20,446) |

Pregunta 6. ¿Cuánto vale tener en cuenta el efecto cruzado? Comparen con la suma de las utilidades propuestas de la parte 3 (12,251 + 8,195). Después, un matiz: según el valor del cliente (CLV), un cliente de Constantes vale unos 306 y uno de Casuales unos 55. ¿Cómo cambia eso la lectura de la ganancia?

| Respuesta del grupo: |

## 5 · Churn máximo (15 min)

Subir el precio deja más margen por cliente, pero puede hacer que se vayan más. El churn máximo c' es el churn hasta el cual el CLV no baja. Para cada segmento: calculen el CLV de hoy con clv(m, c), el margen nuevo m' = precio propuesto − C, y churn_maximo(m', CLV).

| # TU CÓDIGO AQUÍ# 1) clv_hoy = clv(m, c) con m = precio de hoy − costo# 2) m_nuevo = p_prop − costo# 3) churn_maximo(m_nuevo, clv_hoy)# Háganlo para los dos segmentos |

No sabemos cuánto subirá el churn en la realidad. Para compararlo, usen la fórmula churn nuevo = c × (1 + ε(c) × %ΔP), donde ε(c) es la elasticidad del churn (cuántos % sube el churn por cada 1% que sube el precio) y %ΔP es el cambio de precio propuesto (+10% en los dos segmentos). Completen la tabla.

| ε(c) | Churn nuevo Constantes (c = 3%) | ¿Cabe en su churn máximo? | Churn nuevo Casuales (c = 6%) | ¿Cabe en su churn máximo? |
| 0.5 |  |  |  |  |
| 1 |  |  |  |  |
| 2.5 |  |  |  |  |

Pregunta 7. ¿En cuál segmento hay menos margen de error con el churn? ¿Qué significa para la decisión?

| Respuesta del grupo: |

## 6 · Recomendación y riesgos (15 min)

Decidan: subir, mantener o probar con un experimento (una prueba A/B donde parte de los clientes ve el precio nuevo y parte el viejo). Toda decisión necesita una frase de justificación con números de las partes anteriores.

|  | Constantes | Casuales |
| Decisión (subir, mantener o probar) |  |  |
| Precio propuesto |  |  |
| Justificación con números |  |  |
| Efecto cruzado (qué le pasa al otro segmento) |  |  |
| Dos riesgos |  |  |
| Métrica de monitoreo y alerta |  |  |

Pregunta 8. ¿Qué le dirían a la dirección en una frase? Incluyan qué decisión toman, por qué, y qué vigilarán después.

| Respuesta del grupo: |
