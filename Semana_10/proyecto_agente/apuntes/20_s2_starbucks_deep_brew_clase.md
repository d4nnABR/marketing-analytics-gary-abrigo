# Semana 2 · Starbucks Deep Brew, CLV, RFM y BG/NBD (clase)

(diapositiva 1) Marketing Analitycs Actividad No. 2 – Laboratorio Uplift y Churn En nuestra segunda actividad, reforzaremos lo practicado en los Breakout Rooms (2 churn, 3 uplift, 4 Qini) de la Semana # 3, aplicado ahora a la campaña COMPLETA de Starbucks Rewards, 40,000 clientes, cupón de $5, medidos a 60 días (no una muestra de prueba como en los breakout rooms).

(diapositiva 1) A diferencia de los breakout rooms, este dataset trae una columna oculta con el tipo real de cada cliente y su uplift verdadero, que se destapa hasta el final.

(diapositiva 1) 1 – Refuerzo y Material en Github Descargen (clonen o hagan un re-fetch del template) el material de la semana # 3, ubicada en el repo del profesor https://github.com/stanlybolanos/marketing-analytics-base-2026/tree/main/Semana_3 Lo que vimos en clase Breakout 2 — Las dos ventanas Breakout 3 — Los 4 cuadrantes Breakout 4 — La curva Qini Qué aporta a este laboratorio El modelo de riesgo/churn, usado aquí para targetear y ver la pérdida El T-learner (dos modelos, uno por grupo) — solo T-learner, no S-learner ni transformación de clase Evaluar el T-learner con datos que nunca vio 2 – Pasos del Laboratorio 1.

(diapositiva 1) Entrenan un modelo de churn y lo usan para targetear al 30% de mayor riesgo — miden el valor real de esa decisión con el experimento como juez. 2. Programan el T-learner (dos modelos, uno entrenado solo con tratados y otro solo con control) y miden su coeficiente Qini contra el modelo de riesgo. 3. Deciden a quién contactar: prueban varios porcentajes de la base ordenados por uplift estimado, encuentran el óptimo y defienden la cifra con números.

(diapositiva 1) © Todos los derechos reservados Universidad Rafael Landívar URL

(diapositiva 2) 4. La comparación (exclusiva del laboratorio): destapan la columna oculta con el tipo real de cada cliente y su uplift verdadero, y comparan contra lo que su modelo estimó. 3 - Entregables 1. El notebook (laboratorio_final.ipynb) ejecutado de principio a fin, con las preguntas de cada paso respondidas. a. Si Usan Google Colab, compartan el link de su notebook (esto es opcional) b. En Github, creen un Branch llamada “Tarea_Actividad_2_Grupo_NumeroGrupo”) i.

(diapositiva 2) Adjunten el link de su Branch (esto ES obligatorio) 2. Su propia app de Streamlit, construida a partir de streamlit_starter.py (a diferencia de los breakout rooms, aquí sí construyen una app, debe mostrar, como mínimo, la curva Qini de su T-learner y la tabla de políticas del Paso 3, con al menos un control interactivo). a. Adjunten el link de su app streamlit (esto ES obligatorio) 3.

(diapositiva 2) Una tabla con la comparación de diferentes modelos de clasificación que usó para comparar la correlación del uplift y el índice Qini, ejemplo (no son datos reales): Modelo dentro del T-learner Correlación con el uplift real Qini Logística (la del notebook) 0.619 +0.142 Árbol sin límite 0.244 +0.010 Árbol con max_depth=2 0.444 +0.041 Otro modelo 0.839 +0.222 4. Una conclusión de una página: ¿a qué porcentaje de la base contactarían, y por qué?

(diapositiva 2) Usando la comparación del Paso 5 para decir qué tan cerca estuvo su modelo de la verdad. Imaginen que están enviando estas conclusiones al Presidente de Marketing de la empresa, elabore una conclusión profesional acorde a esto. © Todos los derechos reservados Universidad Rafael Landívar URL
