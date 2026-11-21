# Semana 6 · Actividad: segmentación de clientes

Marketing Analytics

Actividad – Segmentación de Clientes

Modalidad – Grupos de trabajo  La entrega de esta actividad es con los grupos de trabajo asignados

Pregunta guía de la sesión: ¿a qué grupos de clientes les hablamos distinto, y cuánto vale cada grupo?

## 1 · Preguntas previas (5 min)

Respondan entre todos, sin buscar nada:

¿Cómo decide hoy una empresa que usted conozca qué ofrecerle a cada cliente? ¿A todos lo mismo, o distinto?

Si pudiera dividir a sus clientes en solo tres grupos, ¿con qué criterio los dividiría?

| Respuesta del grupo: |

## 2 · Segmentar a mano (20 min)

Ejemplo pequeño: tres clientes de una tienda en línea.

| Cliente | Ingreso anual (US$) | Visitas a la web por mes |
| A | 30,000 | 3 |
| B | 32,000 | 15 |
| C | 60,000 | 4 |

Pregunta 1. Sin calcular nada: ¿cuál de B o C se parece más a A? Anoten por qué.

| Respuesta del grupo: |

Ahora midan la "distancia" entre clientes (qué tan distintos son). La distancia entre dos clientes es la raíz de la suma de las diferencias al cuadrado.

Con los números tal cual (dólares y visitas):

A–B: diferencia de ingreso 2,000; diferencia de visitas 12. Distancia ≈ 2,000.

A–C: diferencia de ingreso 30,000; diferencia de visitas 1. Distancia ≈ 30,000.

Pregunta 2. Con ese cálculo, ¿quién está más cerca de A? ¿Les parece razonable, sabiendo que B visita la web 5 veces más que A?

| Respuesta del grupo: |

Ahora pongan las dos variables en la misma escala (estandarizar): dividan cada diferencia entre la desviación típica de la variable. Supongan que la del ingreso es US$20,000 y la de las visitas es 5.

| Pareja | Dif. ingreso ÷ 20,000 | Dif. visitas ÷ 5 | Distancia |
| A–B | 2,000 ÷ 20,000 = 0.1 | 12 ÷ 5 = 2.4 | ≈ 2.40 |
| A–C | 30,000 ÷ 20,000 = 1.5 | 1 ÷ 5 = 0.2 | ≈ 1.51 |

Pregunta 3. ¿Quién está más cerca de A ahora? ¿Qué aprendieron sobre estandarizar antes de segmentar?

| Respuesta del grupo: |

## 3 · Miren los datos antes de usar Orange (15 min)

Esta es una muestra de la base que usarán en el laboratorio: 2,205 clientes de un retailer de alimentos. Todavía no abran Orange. Con lo que ven aquí, respondan.

Seis clientes al azar (columnas seleccionadas):

| id | Ingreso anual (US$) | Edad | Hijos pequeños | Gasto total, 2 años (US$) | Compras web | Compras tienda | Visitas web/mes | Educación |
| 2036 | 42,554 | 42 | 1 | 41 | 2 | 3 | 4 | Licenciatura |
| 749 | 46,891 | 55 | 0 | 122 | 2 | 4 | 4 | Maestría 2.º ciclo |
| 2043 | 54,591 | 71 | 0 | 495 | 6 | 8 | 5 | Licenciatura |
| 8 | 33,454 | 35 | 1 | 146 | 4 | 4 | 8 | Doctorado |
| 1562 | 40,442 | 68 | 1 | 156 | 3 | 4 | 7 | Maestría |
| 1404 | 38,741 | 62 | 1 | 48 | 2 | 3 | 7 | Maestría 2.º ciclo |

Resumen de algunas variables (los 2,205 clientes):

| Variable | Mínimo | Mediana | Promedio | Máximo |
| Ingreso anual (US$) | 1,730 | 51,287 | 51,622 | 113,734 |
| Edad | 24 | 50 | 51 | 80 |
| Gasto total, 2 años (US$) | 4 | 343 | 563 | 2,491 |
| Días desde la última compra | 0 | 49 | 49 | 99 |

Pregunta 4. ¿Qué creen que son estos datos? ¿Qué tipo de negocio es y quiénes son sus clientes? ¿Qué les llama la atención? (Pista: miren el gasto total, la mediana y el promedio.)

| Respuesta del grupo: |

Pregunta 5. Hipótesis. Si tuvieran que dividir estos clientes en tres grupos, ¿cuáles serían? Descríbanlos antes de ver ningún resultado:

| Grupo (nombre) | Cómo es: ingreso, gasto, compras | % de clientes que esperan | % del gasto que esperan |
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

Pregunta 6. ¿Qué dato les haría cambiar de opinión sobre estos grupos? ¿Qué variable creen que separa más a los clientes?

| Respuesta del grupo: |

## 4 · Laboratorio de Orange (≈60 min)

Pregunta de negocio: ¿a qué grupos de clientes les hablamos distinto, y cuánto vale cada grupo?

Se hace después de la presentación. Sigan los pasos tal como están y respondan, en cada parte, las preguntas del laboratorio y las de hallazgos.

### Archivos

| Archivo | Qué es |
| clientes_retail.csv | Real. 2,205 clientes de un retailer de alimentos (versión limpia de "Customer Personality Analysis", base abierta). Ingreso, edad, hijos, gasto por categoría, compras por canal, recencia y respuesta a campañas |
| formas_lunas.csv | Sintético. 400 puntos en forma de dos lunas + 20 de ruido. Sirve para ver dónde falla k-means |
| formas_alargadas.csv | Sintético. 3 grupos alargados e inclinados. Sirve para el notebook (mezclas gaussianas) |

Nota: gasto_total ya es la suma de vinos, frutas, carnes, pescado y dulces. gasto_premium es una parte de ese total, no se suma.

Aviso: los archivos formas_* son datos creados para el ejercicio y no son clientes reales. El archivo clientes_retail.csv es real y proviene de una base abierta.

### Parte 1 · Conozca los datos (10 min)

1. File → clientes_retail.csv. Conecte Data Table y Distributions (gasto_total).

2. ¿Cómo se ve gasto_total? (Pocos clientes gastan mucho, muchos gastan poco.)

Hallazgo. ¿La forma de gasto_total coincide con lo que vieron en la Pregunta 4 (mediana 343, promedio 563)? ¿Qué significa para un promedio?

| Respuesta del grupo: |

### Parte 2 · k-means: el punto de partida (15 min)

1. Select Columns: deje como atributos solo ingreso_anual, gasto_total, compras_tienda, compras_web, compras_catalogo, visitas_web_mes, recencia_dias, hijos_pequenos, edad. Todo lo demás a "Ignored" o "Meta".

2. Continuize / Normalize (estandarizar por desviación): si no se normaliza, el ingreso (decenas de miles) aplasta a las visitas web (unidades).

3. k-Means con "From 2 to 8" y mire la silueta de cada k.

4. Fije k = 3 y conecte a Scatter Plot (x = ingreso_anual, y = gasto_total, color = Cluster).

5. Group By (o Box Plot por Cluster): promedio de cada variable por segmento.

Preguntas del laboratorio: ¿qué k tiene mejor silueta? ¿Es muy alta? ¿Ponga un nombre de negocio a cada segmento?

| Respuesta del grupo: |

Pregunta 7 (contraste con su hipótesis). Anoten lo que encontraron y compárenlo con la Pregunta 5.

| Segmento (nombre de negocio) | Clientes | Ingreso promedio | Gasto promedio | ¿Se parece a su hipótesis? ¿Qué los sorprendió? |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

Capture aquí el Scatter Plot de k-means (k = 3).

| Respuesta del grupo: |

### Parte 3 · Compare técnicas (15 min)

1. Con los datos normalizados, conecte Distances (Euclidean) → Hierarchical Clustering (Ward). Corte en 3 grupos.

2. Conecte los datos normalizados a DBSCAN. Use el gráfico de distancia al k-ésimo vecino para escoger eps; pruebe cerca de 1.5 y compare con 2 o 3.

3. Compare cuántos clientes caen en cada grupo con cada técnica (Merge Data o Scatter Plot coloreado).

Preguntas del laboratorio: ¿las tres técnicas dan los mismos grupos? ¿Qué pasa con DBSCAN al subir eps? ¿Cuál le serviría más a marketing para actuar?

| Respuesta del grupo: |

Pregunta 8. Una segmentación puede ser estadísticamente correcta y no servir para nada. Un segmento útil cumple cinco condiciones:

| Condición | Significa |
| Medible | Se puede calcular con datos que tenemos |
| Diferenciable | Los grupos se comportan distinto entre sí |
| Accionable | Podemos hacer algo distinto con cada uno |
| Rentable | El grupo es lo bastante grande o valioso |
| Estable | No cambia por completo cada mes |

Evalúen las tres técnicas de esta parte con sus propios resultados (sí / parcial / no) y recomienden una. ¿Alguna no sirve en absoluto?

| Técnica | Medible | Diferenciable | Accionable | Rentable | Estable | Nº de grupos y ruido |
| k-means (k = 3) |  |  |  |  |  |  |
| Jerárquico (Ward, 3 grupos) |  |  |  |  |  |  |
| DBSCAN (su eps) |  |  |  |  |  |  |
| Respuesta del grupo: |

### Parte 4 · ¿Cuánto vale cada segmento? (10 min)

1. Con los grupos de k-means (k = 3), calcule por segmento: número de clientes, gasto promedio y % del gasto total (Group By + Formula).

2. Mire también respondio_ultima_campana por segmento.

Preguntas del laboratorio: ¿qué % de clientes genera qué % del gasto? ¿A qué segmento le gastaría el presupuesto de la próxima campaña y por qué? (Recuerde el CLV/CAC de las semanas anteriores.)

Guarde su segmentación (la usará en la tarea):

1. Conecte la salida Data de k-Means (k = 3) a Save Data.

2. Formato CSV, nombre clientes_con_cluster.csv.

3. Ábralo y compruebe que trae la columna Cluster con los valores C1, C2 y C3.

Nota: lo más simple en Orange es guardar la asignación de cada cliente. Un archivo .joblib no es el formato de Orange; los modelos de Python (notebook) sí se guardan así.

Valor por segmento (con sus resultados):

| Segmento | Clientes | % de clientes | Gasto medio (US$) | % del gasto total | % que respondió la última campaña |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

Pregunta 9. Un grupo pequeño de clientes suele generar la mayor parte del gasto. ¿Qué encontraron? ¿Qué haría distinto con cada segmento (retener, crecer, adquirir, no invertir)? Conecten con lo visto antes: CLV, CAC y razón CLV/CAC.

| Respuesta del grupo: |

Pregunta 10 (cálculo). Ejercicio ilustrativo: suponga un margen de 20% sobre el gasto y una campaña que cuesta US$10 por cliente contactado. Con el gasto medio de su tabla, calculen el margen de un cliente de dos años en el segmento de más gasto y en el de menos, y comparen con el costo de la campaña.

Pista: margen = 20% × gasto medio. ¿En qué segmento conviene más gastar los US$10?

| Respuesta del grupo: |

### Parte 5 · Datos sintéticos: cuando k-means falla (10 min)

1. File → formas_lunas.csv. Scatter Plot (x, y; color = grupo_real).

2. k-Means con k = 2 y mire cómo parte las lunas. Luego DBSCAN directo sobre x e y (sin estandarizar): pruebe eps ≈ 0.2 y min vecinos = 5. Pruebe también eps = 0.1.

3. Compare con grupo_real.

Preguntas del laboratorio: ¿por qué k-means corta mal? ¿Qué hizo DBSCAN con el ruido? ¿Cuándo sospecharía que sus clientes no tienen forma de "bolas"?

| Respuesta del grupo: |

Pregunta 11. En los clientes reales, DBSCAN dio un resultado distinto al de las lunas. ¿Por qué funcionó en un caso y no en el otro? ¿Qué le diría a un gerente que quiere "la técnica más moderna"?

| Respuesta del grupo: |

Lo que Orange no trae (mezclas gaussianas y k-prototypes) está en el notebook, que es parte de la tarea.

## 5 · Riesgos de segmentar (10 min)

Pregunta 12. Las variables de la base incluyen edad, hijos y estado civil. ¿Es correcto segmentar con ellas? ¿Dónde está el límite entre personalizar y discriminar o invadir la privacidad?

| Respuesta del grupo: |

Pregunta 13. Los segmentos cambian: un cliente de bajo gasto puede crecer, y uno de alto valor puede irse. ¿Cada cuánto recalcularían la segmentación y qué señales vigilarían?

| Respuesta del grupo: |

## 6 · Conclusiones (10 min)

Escriban en tres líneas qué segmentación recomendarían a marketing, con qué técnica y qué acción tomarían con el segmento más valioso.

| Respuesta del grupo: |

## Anexo · Notebook de la tarea: mezclas gaussianas y k-prototypes

Lo que Orange no trae. Se hace después de la sesión, en casa, como parte de la tarea. Son seis pasos, de arriba hacia abajo.

### Pasos

1. Abra el notebook en Google Colab (colab.research.google.com → Archivo → Subir cuaderno) o en Jupyter. El archivo es notebook_segmentacion.ipynb.

2. Suba los dos CSV junto al notebook: clientes_retail.csv y formas_alargadas.csv. En Colab: ícono de carpeta a la izquierda → Subir. El notebook no usa formas_lunas.

3. Ejecute las celdas en orden, de arriba hacia abajo (Mayús + Enter en cada una). La primera instala kmodes y tarda unos segundos.

4. Sección 1 · Mezclas gaussianas. Con formas_alargadas.csv, compare k-means y GMM contra la respuesta real (grupo_real). La segunda celda cuenta los puntos "con duda" (son datos sintéticos, no clientes): los que no tienen ninguna probabilidad mayor a 0.9.

5. Sección 2 · K-prototypes. Con clientes_retail.csv, segmente con números y categorías (educación y estado civil) en un solo modelo.

6. Sección 3 · ¿Coinciden con k-means? Compare k-prototypes contra k-means: el acuerdo (1 = idénticos) y la tabla cruzada.

### Preguntas

Pregunta N1. ¿Por qué GMM acierta más que k-means con los grupos alargados? ¿Qué ventaja extra tiene (pista: da una probabilidad de pertenecer a cada grupo)?

| Respuesta del grupo: |

Pregunta N2. ¿Cuántos puntos quedaron "con duda"? Si fueran clientes reales, ¿qué haría marketing con ellos en vez de forzarlos a un solo grupo?

| Respuesta del grupo: |

Pregunta N3. ¿Agregar educación y estado civil (k-prototypes) cambió los grupos respecto a k-means? ¿Cambia el gasto medio por segmento según la técnica?

| Respuesta del grupo: |

Pregunta N4. ¿Qué segmentación le daría a marketing y por qué? Contesten en 3 líneas, con la técnica y la acción que tomarían.

| Respuesta del grupo: |

### Guarde sus resultados

La última sección (4) guarda lo que usará en la app de Streamlit. Ejecute esa celda al final y compruebe que se crearon los tres archivos:

| Archivo | Qué contiene |
| segmentos_notebook.csv | La asignación de cada cliente (columnas seg_kmeans, seg_gmm, seg_kproto y Cluster). Es lo que sube al visor de la app |
| modelo_gmm.joblib | El modelo de mezclas gaussianas ajustado, con su estandarizador y la lista de variables |
| modelo_kproto.joblib | El modelo de k-prototypes ajustado, con las variables numéricas y categóricas |

Nota: la columna Cluster toma la técnica que usted recomienda (por defecto k-prototypes). Cámbiela en la celda si prefiere otra.

### Entregable

Este documento con las respuestas del grupo.

Capturas del laboratorio de Orange: Scatter Plot de k-means (k = 3), árbol jerárquico cortado en 3 grupos, gráfico de distancia de DBSCAN con su eps, y la tabla de valor por segmento.

Formato: PDF, entregado por Teams.

Tarea, después de la sesión: el notebook ejecutado (con sus archivos segmentos_notebook.csv y los dos .joblib) y la app en Streamlit (app.py y requirements.txt), según TAREA_Segmentacion.
