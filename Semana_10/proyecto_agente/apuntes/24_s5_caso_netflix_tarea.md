# Semana 5 · Tarea: Caso No. 2 Netflix, CLV y recomendación

Marketing Analytics

Caso No. 2 – Netflix: del algoritmo al CLV

Modalidad – Grupos de trabajo  Primera parte de la sesión: 1 hora y 30 minutos de trabajo en grupo. Después viene el receso, la presentación y, al final, el laboratorio de Orange. La entrega es con los grupos de trabajo asignados

En esta actividad cerramos el ciclo de la fórmula del CLV con un solo caso: Netflix. Van a ver tres videos y discutir el caso; al final de la sesión analizarán datos en Orange. Todo sirve para responder una pregunta de gerencia: de las cuatro palancas del CLV (margen, retención, ARPU y CAC), ¿cuál vale más?

Trabaja en orden. El punto 1 solo funciona si lo haces antes de ver los videos, y el punto 4 y el laboratorio final solo funcionan si el punto 1 ya está escrito.

| Momento | Qué hacen | Tiempo |
| Punto 1 | Preguntas previas | 5 min |
| Punto 2 | Tres videos con preguntas | 30 min |
| Punto 3 | Preguntas del caso | 50 min |
| Punto 4 | Conclusiones del trabajo | 5 min |
| Receso |  |  |
| Presentación | El profesor cierra la fórmula del CLV | aprox. 30 min |
| Punto 5 – Orange | Laboratorio de datos (anexo de este documento) | aprox. 60 min |

Orden de la sesión: Word en grupo, receso, presentación y, de último, Orange. Guarden este documento: el anexo se completa al terminar el laboratorio.

#### 1 – Preguntas previas

Antes de ver los videos, respondan a las siguientes preguntas. No hay respuesta errónea; el objetivo es comparar al final lo que creían con lo que encontraron.

Netflix tiene unos 167 millones de miembros y gasta más de US$2,600 millones al año en marketing. Si pudieran mejorar UNA cosa en 10% (el precio, el costo del contenido, que los clientes cancelen menos o el costo de conseguir clientes), ¿cuál escogen y por qué?

¿Qué porcentaje de lo que la gente ve en Netflix creen que viene de una recomendación y no de buscar un título a propósito?

¿Cuál creen que fue el mayor obstáculo de Netflix para crecer? Marquen uno y expliquen en una línea.

El contenido: producir o licenciar lo que la gente quiere ver.

Retener: que los clientes no cancelen después del primer mes.

Adquirir: que cada cliente nuevo cueste menos de lo que vale.

Otro:

#### 2 – Videos – Contexto del caso Netflix

##### Video 1 – Netflix Research: cómo explican sus recomendaciones

Los videos a continuación no forman parte del caso de Harvard, pero dan contexto que enriquecerá la discusión.

Video del canal de Netflix: Netflix Research: Recommendations

https://www.youtube.com/watch?v=4aNfPe-pQqI

Es un video de la propia empresa, así que véanlo con ojo crítico: muestra lo que Netflix quiere mostrar de sus recomendaciones.

Respondan a las siguientes preguntas

a) ¿Qué datos usa Netflix de ti sin que tengas que escribir nada?

b) ¿Qué recibes tú a cambio de esos datos?

c) El video no lo dice: ¿cómo sabría Netflix que su recomendación realmente hizo que alguien se quedara?

##### Video 2 – El Netflix Prize contado por quienes lo ganaron

Dos investigadores de AT&T Labs, Chris Volinsky y Robert Bell, formaron parte del equipo que ganó el concurso de US$1 millón de Netflix.

From the Labs: Winning the Netflix Prize (AT&T Tech Channel)

https://www.youtube.com/watch?v=ImpV70uLxyw

Respondan a las siguientes preguntas

a) ¿Qué estaban tratando de predecir y cómo se mide si lo hicieron bien (RMSE)?

b) Netflix pagó el premio, pero después dijo que no puso en producción el algoritmo ganador completo. ¿Por qué creen que un modelo mejor en el concurso no era necesariamente mejor para el negocio?

##### Video 3 – Netflix contra Disney en una entrevista

Entrevista de Bloomberg Tech: Streaming Wars: Disney Vs. Netflix. Es posterior al caso, así que sirve para ver cómo cambió el panorama.

https://www.youtube.com/watch?v=pRnhRy-vOt8

Respondan a las siguientes preguntas

a) ¿Qué palanca del CLV (margen, retención, ARPU, CAC) creen que amenaza más Disney? ¿Por qué?

b) ¿Qué argumento del entrevistado les parece más débil o menos probado con datos?

#### 3 – Preguntas del Caso: Netflix vs. Disney (50 min)

Después de leer el caso Netflix vs. Disney (Darden, UV7905), que se obtiene en el portal de Harvard Business Publishing, cada integrante escoge una de las preguntas 1 a 5, la responde en unos 10 minutos y se la explica al resto del grupo. Después llenan la tabla de ventajas, hacen el ejercicio de la franquicia y discuten la pregunta 6.

Pregunta 1 – Claves del éxito. ¿Cuáles son las claves del éxito de Netflix y qué métricas de clientes le importan más? (Palanca: retención y CLV)

Pregunta 2 – Por qué Disney+. ¿Por qué lanza Disney su propio servicio, y qué le permite hacer cobrar menos que Netflix? (Palanca: margen)

Pregunta 3 – Cómo compite Netflix. ¿Cómo puede competir Netflix con Disney+? Antes de llenar la tabla de abajo, anoten sus ideas sin filtrar. (Todas las palancas)

Pregunta 4 – Valor a lo largo de la vida del cliente. ¿Cómo mejora Netflix lo que ofrece a cada cliente con el tiempo, y qué efectos de red hay (más clientes → mejores recomendaciones)? (Palanca: ARPU y retención)

Pista: relacionen con la cadena de los videos: recomendar → encontrar rápido → quedarse → CLV más alto.

Pregunta 5 – ¿Caben los dos? ¿Pueden sobrevivir Netflix y Disney+, o solo uno? Piensen en un cliente con ambos servicios a la vez y en cuánto está dispuesto a pagar. (Palanca: precio y CAC)

##### Tabla de ventajas competitivas

Para cada fuente de ventaja, marquen si Netflix la tiene frente a Disney+ (++ clara, + parcial, − no) según estas condiciones: valiosa, no sustituible, inimitable y rara. Justifiquen en una línea la fuente que marquen más fuerte.

| Fuente de ventaja | Valiosa | No sustituible | Inimitable | Rara |
| Economías de escala |  |  |  |  |
| Efectos de red (datos y algoritmos) |  |  |  |  |
| Contraposición al modelo anterior |  |  |  |  |
| Costos de cambio |  |  |  |  |
| Marca |  |  |  |  |
| Recurso exclusivo |  |  |  |  |
| Poder de proceso |  |  |  |  |

##### Ejercicio – ¿Cuánto vale una franquicia como Star Wars?

Cuando Netflix negocia la licencia de una franquicia, puede estimar cuánto valor le daría a sus clientes con esta idea: el valor es la parte del tiempo total de visualización que esperamos que se vaya a esa franquicia, multiplicada por el presupuesto de contenido.

Valor de la franquicia = (tiempo de visualización esperado de la franquicia ÷ tiempo total de visualización) × presupuesto de contenido

Números ilustrativos, inventados para el ejercicio: presupuesto de contenido anual de US$10,000 millones.

| Parte del tiempo total de visualización | Valor de la franquicia |
| 1% | US$100 millones (ejemplo resuelto) |
| 2% |  |
| 3.5% |  |

Si el dueño de la franquicia pide US$300 millones al año, ¿para qué porcentajes del tiempo de visualización conviene pagar?

¿Qué dato del algoritmo de recomendación le ayuda a Netflix a estimar ese porcentaje antes de comprar?

¿Con qué palanca de la fórmula del CLV se relaciona este cálculo, margen, retención, ARPU o CAC? Expliquen en una frase.

Pregunta 6 – Una tensión. Se dice que, como Netflix ya es una marca muy conocida, le conviene concentrarse en retener clientes y no tanto en conseguir nuevos. ¿Están de acuerdo? Escriban su hipótesis ahora; la comprueban con los datos de canales en Orange.

Debate: cada persona defiende que su palanca es la que más debería proteger el presupuesto del próximo año. Anoten el mejor argumento a favor y el mejor en contra.

| Palanca | Argumento a favor | Argumento en contra |
| EJEMPLO Retención: bajar el churn 0.5 punto vale más que subir el precio 10% porque … |  |  |
|  |  |  |
|  |  |  |

##### Recomendación: Humano vs. Robot

Ahora cada uno tome un minuto para recomendar una película y/o serie al resto de sus compañeros:

| Integrante | Recomendación | Feedback |
| Ejemplo: Juan Perez | Ejemplo: Amigos buscan series de suspenso, Juan recomienda la serie de “Stranger Things”, posiblemente alguien además de Juan confirma dicha recomendación. | Ejemplo: Los integrantes del grupo de Juan encuentran la recomendación de Juan acertada |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

¿Consideran “confiar más” en recomendaciones de amigos y/o conocidos que las del sistema de recomendación?

¿Han tenido “malas experiencias” con una recomendación de Netflix? Es decir les recomendó una película o serie que no les gusto, y de ser así después de marcar el “thumbs down” (pulgar abajo) ¿creen que mejoró?

#### 4 – Conclusiones del trabajo (5 min)

Vuelvan a las preguntas del punto “1 – Preguntas previas”. Lean lo que escribieron sin corregirlo.

a) ¿Cambiaron de opinión sobre la palanca que escogieron? ¿Por qué?

b) El obstáculo que marcaron en el punto 1, ¿era el correcto según los videos y el debate?

c) Para cada palanca (margen, retención, ARPU, CAC), escriban qué dato les haría falta para saber cuánto vale de verdad. Guarden esa lista: la van a revisar con los datos de Orange al final.

#### 5 – Anexo: laboratorio de Orange (al final de la sesión)

Este anexo se completa después de la presentación, con la guía GUIA_LAB_Netflix_Orange ubicada en la semana # 5 del repo de GitHub: https://github.com/stanlybolanos/marketing-analytics-base-2026/tree/main/Semana_5/orange_lab.

Archivos: la carpeta del laboratorio con 12,000 suscriptores simulados de Netflix, el gasto de marketing, y la cantidad de calificaciones reales de 10,506 películas (MovieTweetings). Sigan la guía GUIA_LAB_Netflix_Orange. Los suscriptores son simulados, no son datos de Netflix.

Fórmula: CLV = margen × (1 − churn) ÷ (churn + 0.008). Churn mensual = bajas ÷ meses observados. CAC = gasto ÷ altas.

##### 5.1 – La pantalla personalizada contra la de populares

Usando Group By por home_experimento, calculen la retención a 12 meses de cada grupo, el churn y el CLV.

¿Cuántos puntos más retiene la pantalla personalizada y cuánto vale por cliente? ¿Por qué podemos decir que la causó?

| Grupo | Retención a 12 meses | Churn mensual | CLV por miembro |
| Personalizada |  |  |  |
| Popular |  |  |  |
| Diferencia |  |  |  |

##### 5.2 – CLV y CAC por canal

Calculen por canal el CAC, el churn, el CLV y la razón CLV/CAC. Marquen en el Bar Plot cuáles pasan de 3.

| Canal | CAC | Churn | CLV | CLV/CAC |
| Referidos y orgánico |  |  |  |  |
| Búsqueda de pago |  |  |  |  |
| Alianzas (telcos) |  |  |  |  |
| Redes sociales |  |  |  |  |
| TV y exteriores |  |  |  |  |

##### 5.3 – ¿Qué predice que un suscriptor se quede?

En Test and Score comparen los cuatro modelos. Anoten AUC y CA, y qué pasa cuando le ponen límite de profundidad al árbol.

¿Le gana algún modelo a "siempre responder la mayoría" en CA? ¿Y en AUC? ¿Las variables principales del Rank se pueden mover para retener, o son solo señales?

| Modelo | AUC | CA |
| Constant (mayoría) |  |  |
| Regresión logística |  |  |
| Árbol con límite 4 |  |  |
| Árbol sin límite |  |  |
| Random Forest |  |  |

##### 5.4 – Datos reales: la cola larga

¿Qué porcentaje de las 10,506 películas tiene menos de 5 calificaciones? ¿Cuáles son las tres más calificadas?

Con esa concentración, ¿qué tanto ayuda personalizar? (Un dato extra: recomendar las 10 más populares acertó 14.5% de las veces y un recomendador personalizado, 15.4%.)

##### 5.5 – Conecten con la verdad oculta: cuántos habrían llegado igual

Conecten con la verdad oculta (verdad_oculta_resumen.csv) y calculen el CAC real y la razón CLV/CAC real. ¿Por qué bajó la razón en todos los canales? ¿Qué canal se veía mejor de lo que era y cuál cambió de lugar? Fíjense en el orden de las barras, no solo en la altura.

| Canal | CLV/CAC contable | Habría llegado igual | CAC real | CLV/CAC real |
| Referidos y orgánico |  |  |  |  |
| Búsqueda de pago |  |  |  |  |
| Alianzas (telcos) |  |  |  |  |
| Redes sociales |  |  |  |  |
| TV y exteriores |  |  |  |  |

##### 5.6 – Conclusión con datos

Vuelvan a la lista del punto 4c. ¿Qué dato de los que pidieron lo pudieron calcular en Orange, y cuál sigue sin respuesta? ¿Cambia su respuesta a la pregunta del punto 1?

#### Entregables

Este documento con los puntos 1, 2, 3 y 4 respondidos y el anexo de Orange (punto 5) completo.

Una conclusión de una página: ¿en qué palanca debería poner Netflix el próximo dólar? Usen los números del laboratorio (punto 5) y digan cuáles son reales (los reportes anuales y las calificaciones de películas), cuáles son supuestos y cuáles son simulados. Imaginen que están enviando estas conclusiones al Presidente de Marketing de la empresa, elaboren una conclusión profesional acorde a esto.

Nota: Los suscriptores y el gasto son simulados. Las calificaciones de MovieTweetings son de uso libre con atribución (Dooms, De Pessemier y Martens, 2013).
