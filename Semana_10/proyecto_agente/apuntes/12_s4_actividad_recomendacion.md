# Semana 4 · Actividad: recomendación

Marketing Analytics

Actividad No. 3 – Laboratorio de Recomendación

En nuestra tercera actividad, reforzaremos lo practicado en los Breakout Rooms (2 matriz y coseno, 3 filtrado por ítem y por cliente, 4 comparar y medir) de la Semana # 4, aplicado ahora a una cafetería con 8,000 clientes, unos 10 meses de historial de compras y un experimento de 90 días con el carrusel “Para ti” (no el dataset de práctica de los breakout rooms).

A diferencia de los breakout rooms, el experimento trae un grupo de control que no vio el carrusel, y el laboratorio guarda información oculta (qué compraría cada cliente por su cuenta y cuánto cambia el carrusel su decisión) que se destapa hasta el final.

#### 1 – Refuerzo y Material en Github

Descargen (clonen o hagan un re-fetch del template) el material de la semana # 4, ubicada en el repo del profesor

https://github.com/stanlybolanos/marketing-analytics-base-2026/tree/main/Semana_4

| Lo que vimos en clase | Qué aporta a este laboratorio |
| Breakout 2 — Matriz y coseno | La matriz cliente × producto y la similitud de coseno, usadas aquí para armar los recomendadores de ítem y de cliente |
| Breakout 3 — Filtrado por ítem y por cliente | Los dos recomendadores (ítem-based y cliente-based) y su puntaje por producto, más un modelo libre a su elección |
| Breakout 4 — Comparar y medir | Medir con datos que nunca vieron (holdout de 90 días) y juzgar con el experimento si el carrusel realmente genera ingreso extra |

#### 2 – Pasos del Laboratorio

Construyen la matriz cliente × producto y los recomendadores (ítem-based, cliente-based y un modelo libre a su elección) más la popularidad como línea base — cada uno entrega el top 3 de productos que el cliente aún no compra.

Evalúan con el holdout de 90 días: hit rate@3, precisión@3 y cobertura, solo con el grupo de control (el que no vio el carrusel).

Miden con el experimento A/B: ARPU con su intervalo de confianza al 95%, margen neto después del costo del carrusel y CLV usando r/(1+d−r).

Resuelven el arranque en frío: ¿qué recomiendan a los clientes nuevos sin historial? Combinan los recomendadores según el historial disponible.

La comparación (exclusiva del laboratorio): destapan la información oculta del cliente y comparan, para cada recomendador, el hit rate contra el ingreso incremental real, y cuánto de lo “acertado” habría pasado de todos modos.

#### 3 - Entregables

El notebook (laboratorio_recomendacion.ipynb) ejecutado de principio a fin, con las preguntas de cada paso respondidas.

Si Usan Google Colab, compartan el link de su notebook (esto es opcional)

En Github, creen un Branch llamada “Tarea_Actividad_3_Grupo_NumeroGrupo”)

Adjunten el link de su Branch (esto ES obligatorio)

Su propia app de Streamlit, construida a partir de streamlit_starter.py (debe mostrar, como mínimo, 3 recomendaciones por cliente con su “porque”, la tabla de comparación de recomendadores, y al menos un control interactivo).

Adjunten el link de su app streamlit (esto ES obligatorio)

Una tabla con la comparación de los recomendadores que probó, ejemplo (no son datos reales):

| Recomendador | Hit rate@3 (control) | Ingreso incremental (US$/cliente) |
| Popularidad | 0.20 | 0.90 |
| Ítem-based | 0.38 | 1.10 |
| Cliente-based | 0.30 | 1.10 |
| Otro modelo | 0.35 | 1.15 |

Una conclusión de una página: ¿pondrían el carrusel para toda la base, y con qué recomendador? Usando la comparación del Paso 5 para decir si un hit rate alto significa ingreso extra. Imaginen que están enviando estas conclusiones al Presidente de Marketing de la empresa, elabore una conclusión profesional acorde a esto.
