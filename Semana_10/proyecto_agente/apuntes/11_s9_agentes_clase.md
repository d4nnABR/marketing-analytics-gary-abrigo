# Semana 9 · Agentes de IA (clase)

(diapositiva 1) Agentes de IA MARKETING ANALYTICS Cómo un modelo de lenguaje aprende a usar las herramientas del curso · Clase del 16 de noviembre de 2026

(diapositiva 2) Agenda • • • • • Hype Cycle y estadísticas de Agentes Taxonomía de los agentes y cómo funcionan Demo de Agente usando Google AI Demo de playground en DataRobot Comienzo de Hackaton

(diapositiva 3) • Gartner Hype Cycle (ciclo de expectativas) Ayuda a decidir cuándo y cuánto invertir en una tecnología. • Una pequeña empresa puede evitar gastar su presupuesto limitado en algo que está en el pico de la moda pero aún no da resultados, y aprovechar tecnologías que ya llegaron a la meseta y son baratas y confiables. • Una empresa mediana puede usarlo para escoger dónde hacer pilotos acotados sin apostar todo a una promesa. • Una empresa grande puede ordenar su cartera de innovación:

(diapositiva 3) explorar temprano lo que viene, escalar lo que ya está maduro y anticipar el “valle de la desilusión” para no abandonar una tecnología valiosa solo porque el entusiasmo inicial se desinfló. • En todos los casos, el mensaje es el mismo: no adoptar una tecnología porque está de moda, sino porque resuelve un problema concreto en el momento en que la empresa está lista para aprovecharla. https://www.youtube.com/watch?v=jB1RDz9jaj0

(diapositiva 4) HYPE CYCLE DE GARTNER La curva de expectativas de una tecnología Gartner lo publica cada año para separar la moda de lo que ya produce valor Expectativa ↑ 1. Disparador de innovación 2. Pico de expectativas infladas 3. Valle de la desilusión 4. Pendiente de la iluminación 5. Meseta de productividad Aparece la tecnología: demos y prototipos, casi nadie la usa todavía. Todos hablan de ella: muchas promesas, pocos resultados medibles.

(diapositiva 4) Los pilotos fallan y el interés cae; sobreviven quienes resuelven un problema real. Se entiende para qué sirve: aparecen casos repetibles y mejores productos. Uso amplio y estable: la tecnología ya es infraestructura.

(diapositiva 7) Para 2028, al menos 15% de las decisiones del día a día las tomará un agente de IA En 2024 eran 0%. Y 33% del software empresarial traerá agentes integrados, contra menos de 1% en 2024. Fuente: Gartner, comunicado de prensa del 25 de junio de 2025 (predicción).

(diapositiva 10) Mucho entusiasmo, resultados desiguales Apertura · Marketing y agentes de IA 81% 45% 36% 40%+ de los líderes de martech ya prueba o usa agentes de IA dice que los agentes de sus proveedores no cumplen lo prometido de los proyectos de agentes se cancelarán para fines de 2027 Martech = tecnología de marketing. 413 líderes, junio a agosto de 2025. Entre quienes ya tienen agentes en piloto o en producción.

(diapositiva 10) del trabajo de marketing se automatizaría con IA en 2028 (16% en 2026) Expectativa de los líderes de marketing encuestados. Por costos, valor poco claro o falta de control de riesgos. La pregunta no es "¿uso agentes?", sino "¿cómo construyo uno que dé números correctos y que yo pueda auditar?". Fuentes: Gartner, comunicados del 29 de octubre de 2025 (81%, 45%), 11 de mayo de 2026 (16→36%) y 25 de junio de 2025 (40%+).

(diapositiva 12) Cuatro escalones, de menos a más autonomía 1 · Qué es un agente 1 Chatbot con LLM Responde con lo que "sabe". No calcula ni consulta nada. Puede inventar cifras. 2 LLM aumentado (RAG) Tiene herramientas, búsqueda y memoria, pero hace una sola llamada. Definiciones: Anthropic, "Building effective agents" (diciembre de 2024). 3 Flujo fijo (workflow) El programador define los pasos con código. El LLM rellena cada paso. 4 Agente El LLM decide qué herramienta usar, en qué orden y cuándo terminar.

(diapositiva 13) Las cinco piezas de un agente 1 · Qué es un agente 1 2 3 4 5 Cerebro (LLM) Herramientas Ciclo Memoria Reglas Entiende la pregunta, planea y decide el siguiente paso. Funciones de código: calcular_clv, segmentar_clientes, proponer_precio… Pensar → usar herramienta → observar → repetir hasta terminar. El historial de la conversación y los apuntes que puede consultar. Instrucciones, límites en código y aprobación humana. Analogía:

(diapositiva 13) un analista junior (el LLM) con calculadora y Excel (herramientas), una libreta (memoria) y el manual del jefe (reglas), que pide firma para lo delicado.

(diapositiva 14) ¿Agente o no? Poll 1 · Qué es un agente A B C D Un correo automático de "te extrañamos" cada 30 días sin compra ChatGPT que redacta el texto de una campaña cuando se lo pido Un asistente que lee el churn, decide a quién contactar y propone un presupuesto Un tablero de Power BI que se actualiza cada mañana Regla fija programada. Una sola respuesta, sin herramientas. Elige pasos y herramientas. Reporte programado.

(diapositiva 15) El ciclo del agente: pensar → actuar → observar 2 · Cómo funciona por dentro 1 2 3 4 Pensar Actuar Observar Repetir o responder El LLM lee la pregunta y lo que ya sabe, y decide: ¿respondo o uso una herramienta? Pide una herramienta con sus datos: calcular_clv(12, 0.03). El código la ejecuta y le devuelve el resultado: {"clv": 306.32}. Si le falta algo, vuelve al paso 1. Si ya tiene todo, explica la respuesta. Este patrón se conoce como ReAct (Reasoning + Acting: razonar y actuar).

(diapositiva 15) Un tope de pasos (max_pasos) evita que el agente se quede dando vueltas para siempre. ReAct: Yao y otros (2022), "ReAct: Synergizing Reasoning and Acting in Language Models".

(diapositiva 16) LLM Base – Gemini para nuestro lab Tool calling (herramientas) Temperature – Consistencia Elementos que lo hacen funcionar Manual de instrucción – guía explicita de pasos MCP – conexiones a otros sistemas Historial – como obtiene context anterior RAG – Contenido explicito de busqueda Guardrails – como limitamos su proceder autonomo

(diapositiva 18) Qué ve el LLM de una herramienta 2 · Cómo funciona por dentro · Tool calling (uso de herramientas) def calcular_clv(margen_mensual: float, churn_mensual: float) -> dict: """Calcula el CLV con la fórmula del curso: CLV = m × (1 − c) ÷ (c + d), d = 0.8% mensual. margen_mensual: margen por cliente al mes (US$). churn_mensual: proporción que se va cada mes.""" m, c = margen_mensual, churn_mensual return {"clv":

(diapositiva 18) round(m*(1-c)/(c+0.008), 2)} Lo que el LLM SÍ ve Nombre, parámetros con su tipo y el docstring (el texto entre comillas triples). Lo que NO ve El código. Por eso el docstring es la instrucción de uso: si es confuso, el agente se equivoca. El SDK (kit de desarrollo) convierte la función en una "declaración" JSON. El LLM responde con otro JSON: {"name": "calcular_clv", "args": {"margen_mensual": 12, "churn_mensual": 0.03}}.

(diapositiva 19) Ejemplo paso a paso: "¿Qué precio le pongo a Casuales?" 2 · Cómo funciona por dentro · Pricing Analytics, ejemplo nube fit Persona: Casuales paga $12, cuesta $8, vende 2000. En pruebas: 10.8→2603, 11.4→2274 … 13.2→1576. • Paso 1: pide estimar_elasticidad(precios=[10.8 … 13.2], unidades=[2603 … 1576]) • Resultado: {"elasticidad": -2.5} • Paso 2: pide proponer_precio(precio_actual=12, costo=8, elasticidad=-2.5, unidades_actuales=2000) • Resultado: {"precio_optimo": 13.33, "precio_propuesto":

(diapositiva 19) 13.2, "utilidad_propuesta": 8195, "requiere_aprobacion_humana": true} • Respuesta: "Propongo $13.20 (+10%). La utilidad sube de 8,000 a 8,195. Como el cambio pasa de 5%, necesita aprobación humana." Son los mismos números en la actividad de Nube Fit. La diferencia: aquí el LLM eligió el orden de las herramientas solo.

(diapositiva 21) El Agente sigue un "manual" de instrucciones 2 · Cómo funciona por dentro · System prompt 1 Para cualquier número, usa una herramienta. Nunca calcules de memoria. 2 Antes de explicar un concepto, consulta los apuntes del curso. 3 Si falta un dato, pregunta; no lo supongas. 4 Si un precio requiere aprobación humana, dilo y no lo des por aprobado. 5 Explica en pasos cortos y define cada sigla. El system prompt (instrucciones del sistema) define el rol, el tono y las reglas.

(diapositiva 21) Las reglas importantes también se programan en código: el texto se puede ignorar, el código no.

(diapositiva 22) Memoria: lo que el agente recuerda 2 · Cómo funciona por dentro Memoria corta: el historial Ventana de contexto Memoria larga Cada llamada envía toda la conversación: preguntas, pedidos de herramientas y resultados. Por eso puede responder "¿y qué hago con ese segmento?". Cuánto texto cabe en una llamada, medido en tokens (pedazos de palabra). Más historial = más costo y más lento.

(diapositiva 22) Datos guardados fuera del modelo (archivos, bases de datos) que el agente consulta con una herramienta cuando los necesita. El LLM no "aprende" de la conversación: no cambia por dentro. Solo ve lo que le volvemos a enviar en cada llamada.

(diapositiva 23) RAG: buscar antes de contestar 2 · Cómo funciona por dentro · Retrieval-Augmented Generation 1 2 3 Buscar Aumentar Generar La herramienta buscar_apunte("uplift") trae el apunte del curso. El apunte se agrega a lo que el LLM tiene a la vista. El LLM explica con esa información, no solo con lo que "recuerda". RAG = Retrieval-Augmented Generation (generación aumentada con recuperación). Reduce invenciones porque el agente cita una fuente que nosotros controlamos.

(diapositiva 24) oy no usaremos MCP: nuestras herramientas viven en el mismo notebook. Pero es el camino para llevar un agente a producción con datos de la empresa.

(diapositiva 25) Varios agentes que trabajan juntos 2 · Cómo funciona por dentro · Multiagente y frameworks Multiagente Frameworks Nuestro enfoque Varios agentes con roles: un planificador y un redactor (así es la plantilla Agentic Starter de DataRobot). Librerías que ayudan a armarlos: LangGraph, CrewAI y LlamaIndex. DataRobot trae plantillas para los tres. Llamar al LLM directamente con unas 30 líneas de Python. Así se ve cada paso y se entiende qué pasa. Fuentes:

(diapositiva 25) DataRobot, documentación de Agentic AI; Anthropic, "Building effective agents".

(diapositiva 26) Realidad de los Agentes El 10 de junio de 2025, Salesforce AI Research presentó CRMArena-Pro, un estudio de evaluación integral que revela que los principales agentes de inteligencia artificial alcanzan una tasa de éxito de solo el 58 % en escenarios empresariales de una sola interacción, cifra que cae al 35 % en interacciones de múltiples turnos.

(diapositiva 26) La investigación, detallada en un extenso documento técnico de 31 páginas, analizó 19 tareas empresariales distintas en sistemas de gestión de relaciones con los clientes (CRM).

(diapositiva 27) Errores típicos 3 · Riesgos y diseño responsable Error del agente Qué pasa Inventar números Responde de memoria sin usar la herramienta Usar mal un dato Suma donde iba promedio, o mezcla unidades Suponer lo que falta Rellena un dato en vez de preguntar Herramienta equivocada Elige una función que no corresponde Bucle sin fin Repite pasos sin terminar Las personas y los agentes se equivocan igual. La diferencia es que el agente lo hace más rápido y con más seguridad al hablar.

(diapositiva 28) Guardrails: reglas que el agente no puede romper 3 · Riesgos y diseño responsable · Guardrails Reglas en código Tope de ±10% y precio ≥ 1.2 × costo dentro de proponer_precio. No dependen de que el LLM obedezca. Aprobación humana Si el cambio pasa de 5%, la herramienta lo marca y el agente no puede darlo por hecho. Tope de pasos max_pasos corta el ciclo si se alarga. Controla costo y bucles. Permisos mínimos Solo las herramientas necesarias.

(diapositiva 28) Un tutor no necesita enviar correos ni cambiar precios reales. En el ejemplo de NubeFit pusimos estos Guardrails en forma de restricciones para el optimizador. Bitácora Cada herramienta usada queda registrada con sus datos para auditar después.

(diapositiva 29) ¿Cómo sé si mi agente funciona?

(diapositiva 29) Evaluándolo 3 · Riesgos y diseño responsable · Evaluación Pregunta de prueba Respuesta conocida Herramienta esperada CLV con margen de $12 y churn de 3% 306.32 calcular_clv Churn máximo con margen nuevo de 14 y CLV de 306.32 3.61% churn_maximo_tolerable Precio 20, costo 8, ε = −1.4, 1000 unidades $22 (con aprobación) proponer_precio Lift de A→B con soportes 0.20, 0.25 y 0.08 1.6 metricas_regla_asociacion % del gasto del mejor segmento con k-means (k = 3) 58.9% segmentar_clientes % número correcto % herramienta correcta ¿Pregunta lo que falta?

(diapositiva 29) ¿El número esperado aparece en la respuesta? ¿Usó la función que tocaba? Prueba con datos incompletos.

(diapositiva 30) ¿Cuándo NO usar un agente? 3 · Riesgos y diseño responsable Cuando el camino es fijo Cuando el error es caro Cuando no hay valor claro Si siempre son los mismos pasos, un flujo fijo es más barato, rápido y predecible. Decisiones irreversibles (cambiar precios reales, enviar a toda la base) necesitan una persona. Gartner recomienda usar IA agéntica solo donde entregue valor o ROI (retorno de la inversión) claro. "Agent washing": vender como agente algo que es un chatbot o una automatización.

(diapositiva 30) Gartner estima que solo unos 130 de miles de proveedores de IA agéntica son reales. Fuentes: Gartner, 25 de junio de 2025; Anthropic, "Building effective agents".

(diapositiva 31) Hackaton Semana 10 Construyan un agente experto en todo lo que vimos en el curso UN TUTOR QUE LES SIRVA PARA REPASAR: QUE CALCULE, EXPLIQUE Y VERIFIQUE CHURN, RETENCIÓN, CLV, SEGMENTACIÓN, SISTEMA DE RECOMENDACIÓN Y PRECIOS.

(diapositiva 32) Con qué construir un agente 4 · Herramientas para construir Opción Cómo es Ventaja Para tener en cuenta Colab (VS code) + Gemini Python en el navegador con una llave gratis de Google AI Studio Se ve cada paso; gratis para prototipos Límites de uso por minuto y por día DataRobot: Talk to My Data Agent Subir datos y preguntar en lenguaje natural Casi sin código; gráficos y tablas Función premium DataRobot:

(diapositiva 32) Agentic Starter Plantilla multiagente con backend y frontend Lista para producción y monitoreo Requiere CLI y despliegue: avanzado Streamlit (Interfaz) App web en Python, como en las tareas del curso Interfaz para su agente en la hackathon Guardar la llave en "Secrets", nunca en el código Para la hackathon: Colab o VS Code para construir, Streamlit para mostrar. DataRobot es opcional para equipos que quieran explorarlo.

(diapositiva 33) El toolkit del Agente:

(diapositiva 33) 9 herramientas de todo el curso 4 · Herramientas para construir · Laboratorio Herramienta Qué calcula Clase del curso calcular_clv CLV = m × (1 − c) ÷ (c + d) Semana 1 · Deep Brew churn_maximo_tolerable Churn máximo c' después de un cambio de precio Pricing · Nube Fit valor_campana_retencion Beneficio neto con uplift (efecto incremental) Churn y uplift metricas_regla_asociacion Confianza y lift de A → B Venta cruzada · Apriori relacion_clv_cac CLV/CAC y meses para recuperar el CAC Netflix · CAC estimar_elasticidad ε con regresión ln-ln Pricing analytics proponer_precio P* con reglas y aprobación humana Pricing · Nube Fit segmentar_clientes k-means sobre clientes_retail.csv Segmentación buscar_apunte Apuntes de cada tema (mini RAG) Todo el curso CAC = costo de adquirir un cliente · ε = elasticidad precio · P* = precio óptimo · c = churn mensual · d = 0.8% de descuento mensual.

(diapositiva 37) Fuentes Referencias • Gartner (25 jun. 2025), comunicado: más de 40% de los proyectos de IA agéntica se cancelarán para fines de 2027; 15% de decisiones del día a día autónomas y 33% del software empresarial con IA agéntica para 2028; ~130 proveedores reales. • Gartner (29 oct. 2025), encuesta a 413 líderes de martech (jun.–ago. 2025): 81% prueba o usa agentes; 45% dice que los agentes de proveedores no cumplen lo prometido. • Gartner (11 may. 2026), comunicado:

(diapositiva 37) los líderes de marketing esperan que la automatización con IA del trabajo de marketing pase de 16% en 2026 a 36% en 2028. • Salesforce AI Research (jun. 2025), CRMArena-Pro: ~58% de éxito en tareas de un turno y ~35% en varios turnos. • Anthropic (dic. 2024), "Building effective agents": LLM aumentado, flujos fijos frente a agentes y cinco patrones. • Yao y otros (2022), "ReAct: Synergizing Reasoning and Acting in Language Models".

(diapositiva 37) • DataRobot, documentación de Agentic AI y plantillas de aplicación (consultada en noviembre de 2026). • Los números de los ejemplos se calcularon con las herramientas del laboratorio y coinciden con Nube Fit y Segmentación. • Microsoft Learn, "Copilot Studio overview", y hoja de ruta de Microsoft 365 (aprobación humana para herramientas, 2026).
