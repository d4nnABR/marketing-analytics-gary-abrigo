# Semana 8 · Lab DataRobot, Pricing Analytics (Ritmo)

Marketing Analytics

Lab DataRobot, Pricing Analytics

Pregunta guía: ¿qué precio le recomendamos a cada segmento de Ritmo, y cuánto podemos confiar en el modelo que lo dice?

## Qué vamos a hacer y por qué

Ritmo es una app de suscripción con dos segmentos de clientes, A y B. La empresa quiere saber qué precio cobrar a cada uno. Hoy vamos a responderlo con una herramienta que usan las empresas de verdad: DataRobot, una plataforma que entrena modelos de forma automática (AutoML: machine learning automático).

El plan: entrenar un modelo que aprende cuántas unidades se venden a cada precio, leer de él la elasticidad ε (cuántos % cambian las ventas por cada 1% que cambia el precio), desplegarlo, simular precios en una aplicación y decidir. Al final comparamos con lo que ya sabemos de la clase de precios: P* = C × ε ÷ (1 + ε).

## Plan de las 3 horas

| Tiempo | Qué hacemos | Dónde |
| 0:00 – 0:10 | Introducción: qué vamos a construir | Todos juntos |
| 0:10 – 1:00 | Parte 1: entrenar el modelo y calcular la elasticidad | Breakout rooms |
| 1:00 – 1:15 | Punto de encuentro 1: ¿qué vimos? | Todos juntos |
| 1:15 – 2:00 | Parte 2: desplegar el modelo y simular precios | Breakout rooms |
| 2:00 – 2:15 | Punto de encuentro 2: ¿qué precio y por qué? | Todos juntos |
| 2:15 – 2:50 | Parte 3: ¿y si los precios no se asignaron al azar? | Breakout rooms |
| 2:50 – 3:00 | Conclusión final | Todos juntos |

## Parte 1 · Entrenar el modelo y calcular la elasticidad (50 min)

Archivo de datos: ritmo_diario_experimento.csv. Son ventas diarias de 2024 y 2025 de los dos segmentos, donde el precio de cada día se asignó al azar (como una prueba A/B). Columnas: fecha, segmento, precio, costo, precio_competencia, promocion, dia_semana, mes y unidades.

1. Creen un caso de uso nuevo (Use Case) en DataRobot y suban el archivo ritmo_diario_experimento.csv. Quedará en la lista de activos (Use Case assets). Ahí mismo, más abajo, verán el archivo ritmo_diario_historico.csv para la Parte 3.

Activos del caso de uso: los dos archivos de datos, el experimento y un notebook. Para abrir el notebook hagan clic sobre su nombre (o entren por Notebooks & codespaces en el menú izquierdo).

2. Creen una lista de variables (feature list) llamada Train que tenga todas las columnas menos fecha. Así el modelo no usa la fecha, que no necesitamos.

Cómo: en el menú izquierdo abran Feature lists y elijan crear una lista nueva. Escriban el nombre Train, desmarquen fecha (todas las demás quedan marcadas: 8 de 9) y pulsen Create feature list.

Crear la lista de variables: fecha desmarcada, nombre Train a la derecha.

3. Creen el experimento: en Target feature (variable a predecir) elijan unidades; DataRobot detecta que es de tipo Regression (predice un número). En Training feature list elijan Train. Dejen Modeling mode en Quick Autopilot (modo rápido) y la métrica recomendada, Gamma Deviance.

Configuración del experimento: objetivo unidades, modo Quick Autopilot, métrica Gamma Deviance y lista Train.

4. Inicien el entrenamiento. DataRobot prueba varios modelos y los ordena en el leaderboard (tabla de modelos). Mientras tanto, hagan el paso siguiente.

Leaderboard con los modelos probados. Usen el que dice Prepared for deployment (listo para desplegar): Light Gradient Boosting on ElasticNet Predictions (Gamma Loss), entrenado con el 100% de las filas.

5. Mientras DataRobot entrena, calculen ε con el modelo simple, directamente sobre los datos del archivo. Es la misma regresión log-log de la clase de precios:

| import datarobot as drimport numpy as npimport pandas as pd # Busca en el caso de uso el dataset por su nombre y lo baja como tablads = [d for d in dr.Dataset.list() if d.name == "ritmo_diario_experimento.csv"][0]datos = ds.get_as_dataframe()print(datos.shape) # debe decir (1462, 9) # Pendiente de ln(unidades) contra ln(precio) = elasticidad ε, un segmento por vezfor seg, g in datos.groupby("segmento"): eps = np.polyfit(np.log(g["precio"]), np.log(g["unidades"]), 1)[0] print(f"Segmento {seg}: elasticidad del modelo simple = {eps:.2f}") |

El notebook de DataRobot ya está conectado a su cuenta, por eso encuentra el archivo por su nombre; no hay que subir nada. Puede aparecer un aviso en rojo (FutureWarning): se ignora. Deben ver (1462, 9) y dos elasticidades.

Resultado esperado: A −1.49 y B −2.97.

Anoten estos dos números. Más adelante los comparamos con lo que encuentre DataRobot.

6. Abran el modelo Prepared for deployment, pestaña Explanations, y miren Feature Impact (importancia de variables: cuánto influye cada una). ¿Cuál pesa más?

Feature Impact: el precio es la variable que más pesa, seguida de segmento, mes, día de la semana y precio de la competencia. Data slice dice All data.

7. Abran Feature Effects (efectos de las variables). En Selected feature elijan precio. Este es el gráfico de dependencia parcial: unidades predichas a cada precio.

Feature Effects con precio seleccionado y todos los datos: la curva mezcla A y B. Fíjense dónde termina el eje del precio: el modelo solo vio precios dentro de ese rango.

8. Arriba hay una opción Data slice (un filtro que muestra solo parte de los datos). Creen un slice para segmento A y otro para segmento B (filtrando la columna segmento), y vean una curva por segmento.

Cómo crear cada slice: abran el menú Data slice y elijan Manage slices (administrar slices). Pulsen Add slice (agregar slice), escriban el nombre (segmento A), y en el filtro elijan Filter type = segmento, Operator = (igual), Value = A. Pulsen Add. Repitan para segmento B. Después, en el menú Data slice aparecen las dos para elegirlas.

Menú Data slice: All data, segmento A, segmento B y Manage slices.

Ventana Slices: pulsen Add slice.

Add Slice: nombre, tipo de filtro (segmento), operador (=) y valor (A o B).

Feature Effects con Data slice: segmento A. Precios de $9 a $15; las unidades bajan de unas 101 a unas 47.

Feature Effects con Data slice: segmento B. Precios de $4.5 a $7.5; las unidades bajan de unas 295 a unas 65: el segmento B reacciona mucho más al precio.

9. Con un slice elegido, exporten los datos de la curva (botón Export, opción Partial Dependence, formato .csv). Abran el notebook (clic en su nombre en Use Case assets) y pegarán el texto ahí.

Ventana Export: elijan Partial Dependence y copien el texto csv.

El notebook de DataRobot con la celda de código: el texto exportado va entre las comillas triples de raw_data.

10. En el notebook, calculen ε de cada segmento con esta celda (un slice por vez):

| import ioimport numpy as npimport pandas as pd # Pegue aquí el texto exportado (un slice por vez: A, luego B)raw_data = """Precio,UnidadesVendidas...pega aquí...""" df = pd.read_csv(io.StringIO(raw_data))df = df.dropna() # borra la fila "==Missing==" (precio vacío) # Pendiente de ln(unidades) contra ln(precio) = elasticidad εeps = np.polyfit(np.log(df["Precio"]), np.log(df["UnidadesVendidas"]), 1)[0]print(f"Elasticidad estimada por DataRobot: {eps:.2f}") |

Tres formas de estimar ε. En esta guía usamos las tres y las comparamos:

| Forma | Qué es | Cuánto confiar |
| Cuenta rápida | Dos precios: (% de cambio de las unidades) ÷ (% de cambio del precio). | Depende de qué dos puntos elijan. |
| Modelo simple | Regresión log-log con todos los datos (paso 5). | Estable. |
| DataRobot | Modelo de caja negra; ε se calcula de su curva de dependencia parcial (paso 10). | Estable si el rango de precios es bueno. |

Pregunta 1. ¿Cuánto vale ε en el segmento A y en el B con el modelo simple (paso 5) y con DataRobot (paso 10)? ¿Se parecen? ¿Cuál segmento es más sensible al precio? Anoten también cuánto tardó el entrenamiento.

| Respuesta del grupo: |

Pregunta 2. Miren la forma de la curva del segmento A: baja rápido al principio y luego se aplana. ¿Qué dice eso sobre subir el precio de $12 a $15 comparado con subirlo de $9 a $12?

| Respuesta del grupo: |

Pregunta 3. El modelo de DataRobot es de caja negra (árboles de decisión y una regresión penalizada, ElasticNet) y el modelo simple es una recta. ¿Por qué creen que encuentran la misma elasticidad? (Pista: recuerden cómo se asignaron los precios.)

| Respuesta del grupo: |

## Punto de encuentro 1 (15 min): ¿qué vimos?

¿Qué ε dio cada segmento con el modelo simple y con DataRobot? ¿Coinciden entre sí y con la clase de precios?

¿Qué tuvo que pasar en los datos para que el modelo aprendiera esta curva?

¿Confiarían en la curva fuera del rango de precios que vio el modelo? ¿Por qué? (Lo comprobamos en la Parte 2.)

## Parte 2 · Desplegar el modelo y simular precios (45 min)

1. Registren el modelo (guardarlo en el registro de modelos) y despliéguenlo.

Cómo: abran el modelo Prepared for deployment, pulsen Model actions (acciones del modelo) arriba a la derecha y elijan Register model (registrar modelo). Completen el nombre y confirmen. Se abre la página del modelo registrado, con la etiqueta Ready for deployment (listo para desplegar). Ahí pulsen Deploy (desplegar).

Model actions: Register model.

Modelo registrado (Registered, Ready for deployment). El botón Deploy está arriba a la derecha.

2. Ya con el modelo desplegado, abran el menú Actions (acciones) del modelo y elijan Create application (crear aplicación).

Menú Actions del modelo: Create application.

3. Elijan la plantilla What-if (qué pasaría si) y pulsen el botón para añadir la información de la aplicación (nombre y descripción). Esperen a que la aplicación se cree y ábranla.

Plantillas de aplicación: elijan What-if. (Optimizer es otra plantilla; no la usamos hoy.)

4. La aplicación abre en la página Create Prediction (crear predicción). Aquí hay que darle filas para predecir. Hay tres caminos: Add data (subir un archivo), Add new row (llenar una fila a mano) o Populate averages (rellenar con promedios). Hoy usamos Add data con el archivo escenarios_whatif.csv que les da el profesor.

Página Add Data de la aplicación: suban escenarios_whatif.csv.

Importante: el modelo necesita las 7 variables (precio, segmento, precio_competencia, mes, costo, dia_semana y promocion), no solo el precio. Por eso el archivo trae todas: lo único que cambia entre filas es el precio y el segmento. Si llenan una fila a mano con Add new row, DataRobot les pedirá las siete.

Add New Row: pide las 7 variables del modelo. Populate averages las llena con promedios para probar rápido.

5. Cuando termine la corrida, verán la tabla All Rows (todas las filas) con la predicción de unidades de cada escenario. Los datos de entrenamiento también aparecen en esa tabla; busquen las 16 filas del archivo de escenarios.

Tabla All Rows con la predicción del modelo para cada fila.

6. Hagan clic en una fila y abran el widget What-if and Optimizer. Pulsen Add scenario (agregar escenario) varias veces, cambien solo el precio en cada uno y vean el resultado en Chart (gráfico) o en Table (tabla).

Gráfico What-if con cuatro precios del segmento B: unidades predichas en cada escenario.

7. Ahora pasamos las predicciones del What-if al notebook. (a) En el What-if, con Add scenario, deben tener los 7 precios del segmento B ($4.5, 5, 5.5, 6, 6.5, 7 y 7.5), cambiando solo el precio. (b) En Table (tabla), o pasando el cursor sobre cada punto del gráfico, lean las unidades predichas de cada precio. (c) En la celda de abajo, reemplacen la lista unidades por esos 7 números, en el mismo orden que los precios, y ejecuten. La celda hace tres cosas: calcula la utilidad (P − C) × unidades de cada precio y dice cuál es la mejor; calcula la elasticidad de esas predicciones con la recta log-log; y calcula el precio que da la fórmula P* = C × ε ÷ (1 + ε). Lo que buscamos es ver si el mejor precio calculado con las predicciones del What-if coincide con el de la fórmula.

| import numpy as np C = 4precios = [4.5, 5, 5.5, 6, 6.5, 7, 7.5]unidades = [256.7, 186.3, 139.0, 110.7, 84.1, 68.1, 56.6] # cambie por las suyas for p, u in zip(precios, unidades): print(f"Precio ${p}: unidades {u:.1f} utilidad {(p - C) * u:.1f}") utilidades = [(p - C) * u for p, u in zip(precios, unidades)]print("Mejor precio probado:", precios[utilidades.index(max(utilidades))]) # La fórmula de la clase: P* = C × ε ÷ (1 + ε)eps = np.polyfit(np.log(precios), np.log(unidades), 1)[0]print(f"Elasticidad de estas predicciones: {eps:.2f}")print(f"Precio óptimo con la fórmula: ${C * eps / (1 + eps):.2f}") |

Repitan lo mismo para el segmento A (precios $9 a $15, con C = $4).

8. Comprobación de los límites. El modelo solo vio precios de $9 a $15 en A y de $4.5 a $7.5 en B. Agreguen estos dos escenarios fuera de ese rango al gráfico What-if: A a $20 y B a $12. Están al final del archivo de escenarios.

Escenario individual en What-if. Para agregar los puntos extremos, usen Add scenario y cambien el precio a 20 (A) o 12 (B).

9. Vuelvan a Feature Effects y miren dónde termina la curva (A en $15, B en $7.5). Después, extiendan la recta log-log más allá del último precio probado y comparen con lo que dijo el modelo:

| # Segmento B: ¿qué esperaría la recta log-log a $12, comparado con el modelo?p_fuera = 12pred_modelo = 32.3 # cambie: lo que predijo What-if para B a $12pred_curva = unidades[-1] * (p_fuera / precios[-1]) ** eps # recta log-log extendida print(f"Modelo a ${p_fuera}: {pred_modelo:.1f} unidades, utilidad {(p_fuera - C) * pred_modelo:.0f}")print(f"Recta a ${p_fuera}: {pred_curva:.1f} unidades, utilidad {(p_fuera - C) * pred_curva:.0f}") |

Pregunta 4. ¿Qué precio recomiendan para cada segmento? ¿Cuánta utilidad deja cada uno comparado con el precio de hoy (A: $12, B: $6)?

| Respuesta del grupo: |

Pregunta 5. ¿Coincide el mejor precio que calcularon con las predicciones del What-if (la salida "Mejor precio probado" de la celda del paso 7) con el de la fórmula P* = C × ε ÷ (1 + ε)? Si no coincide, ¿a qué se debe?

| Respuesta del grupo: |

Pregunta 6. ¿Qué predijo el modelo en los puntos fuera del rango (A a $20, B a $12)? Compárenlo con la recta log-log y con el final de la curva de Feature Effects. ¿Por qué no deberíamos fiarnos de esas predicciones?

| Respuesta del grupo: |

## Parte 2b · El optimizador (15 min)

El What-if nos deja probar precios uno por uno. El optimizador (Optimizer) los prueba por nosotros: busca el valor de las variables flexibles (las que nosotros controlamos) que da el mejor resultado. Por defecto maximiza las unidades predichas, pero eso no nos sirve: a menor precio se venden más unidades, y el optimizador siempre escogería el precio más bajo. Lo que queremos es maximizar la utilidad (P − C) × unidades.

Antes de empezar: el optimizador es una aplicación aparte del What-if. Desde el modelo desplegado, abran Actions → Create application y elijan la plantilla Optimizer (en vez de What-if). Pulsen Next: add app info.

Plantillas de aplicación: ahora elijan Optimizer.

Escriban un nombre (por ejemplo, Optimizar precios) y pulsen Create. Esperen a que la aplicación se cree y ábranla.

Nombre de la aplicación y quién puede acceder.

1. En la aplicación, pulsen Build (arriba a la derecha). Abran la página del optimizador (Optimizer Details) y hagan clic sobre el widget What-if and Optimizer.

2. En la pestaña Data, pulsen Manage y dejen solo precio como variable flexible. Si no, el optimizador cambia también el segmento y el precio de la competencia, que nosotros no decidimos.

3. Pulsen Set Constraints (restricciones) y pongan el rango de precio del segmento que van a optimizar: segmento B, Min 4.5 y Max 7.5; segmento A, Min 9 y Max 15. Es un solo rango para toda la aplicación: al cambiar de segmento, cambien también el rango. Pulsen Save.

Set constraints: el rango de precio (aquí 4.5 a 15, el de todos los datos; para optimizar un solo segmento, ajústenlo).

4. En la pestaña Properties, activen Enable scenario optimizer, dejen marcado Maximize y escriban en Custom optimization expression (expresión personalizada de optimización) esta utilidad. Los nombres van entre llaves:

({precio} - {costo}) * {unidades}

Properties: Maximize y el cuadro Custom optimization expression.

5. Agreguen una fila del segmento que van a optimizar (Add new row, o Populate averages cambiando segmento) y esperen la optimización. La fila marcada Optimal es el mejor precio que encontró el optimizador; Actual es la fila original.

Resultado para el segmento B (con el precio de hoy, $6, como fila Actual).

6. Comparen: el precio Optimal, el mejor precio de su celda del paso 7 y el que da la fórmula P* = C × ε ÷ (1 + ε).

Pregunta 7. ¿Qué precio marcó Optimal en el segmento B? ¿Se parece al de la fórmula y al de la celda del paso 7? La utilidad cambia poco entre esos precios: ¿qué significa eso para una recomendación de precio?

| Respuesta del grupo: |

Pregunta 8. Repitan en el segmento A (rango 9 a 15). ¿Dónde cayó el precio Optimal? Si quedó pegado a un borde del rango, ¿por qué no debemos confiar tanto en ese resultado?

| Respuesta del grupo: |

## Punto de encuentro 2 (15 min): ¿qué precio y por qué?

Cada grupo dice su precio por segmento y la utilidad que esperaría.

¿Coincidió el modelo con la fórmula? ¿Qué restricciones del caso de la clase anterior (tope de ±10%, margen mínimo) hay que aplicar antes de proponerlo?

¿Qué predijo el modelo fuera del rango y cuánto se equivocó respecto a la recta?

¿Qué le falta a esta simulación? (Pistas: el churn, el efecto de un segmento sobre el otro.)

## Parte 3 · ¿Y si los precios no se asignaron al azar? (35 min)

Archivo: ritmo_diario_historico.csv. Mismas columnas, pero ahora la empresa subió los precios cuando sabía que había más demanda (diciembre, fines de semana). Es el caso de endogeneidad: el precio no se movió solo.

Repitan lo que hicieron en la Parte 1 pero con ritmo_diario_historico.csv: es el mismo procedimiento con otro archivo de datos. No hace falta desplegar ni usar el What-if: aquí solo importa cómo cambia la elasticidad.

1. Creen un experimento nuevo con ritmo_diario_historico.csv (objetivo unidades, lista Train sin fecha, Quick Autopilot).

2. Calculen ε con el modelo simple: la celda de la Parte 1, cambiando el nombre del dataset en la línea de ds por ritmo_diario_historico.csv.

3. Abran el modelo Prepared for deployment, vayan a Feature Effects con el slice segmento A (y luego B), exporten y calculen ε con la celda de la Parte 1.

4. Comparen las ε con las del archivo del experimento.

Pregunta 9. ¿Cuánto vale ε del segmento A con este archivo? ¿Cómo se compara con la del archivo del experimento? Si usaran esta elasticidad en la fórmula P* = C × ε ÷ (1 + ε), ¿qué precio recomendarían?

| Respuesta del grupo: |

Pregunta 10. ¿Cuál de los dos modelos usarían para fijar el precio real? Expliquen por qué usando la palabra endogeneidad y nombren una forma de corregir el problema (experimento, controles o variable instrumental).

| Respuesta del grupo: |

## Conclusión final (10 min): los hallazgos

Con los datos del experimento (precios al azar) debieron encontrar estas tres cosas. Comparen con sus resultados:

| Hallazgo | Qué debió pasar | Cifras de referencia |
| 1. La ε de DataRobot coincide con la del modelo simple | La caja negra y la recta log-log recuperan la misma elasticidad (iguales hasta el segundo decimal), y las dos se acercan a la verdadera. | A: DataRobot −1.49, modelo simple −1.49, real −1.5. B: DataRobot −2.97, modelo simple −2.97, real −3. |
| 2. El mejor precio del modelo es casi el de la fórmula | El precio con más utilidad, calculado con las predicciones del What-if, coincide con P* = C × ε ÷ (1 + ε). | Segmento B: mejor precio probado $6; fórmula con ε = −2.97 da $6.03. |
| 3. El modelo falla fuera del rango de precios que vio | Un modelo de árboles no extrapola: a precios fuera del rango repite casi el último valor y sobrestima las ventas. | B a $12: el modelo dice 32.3 unidades (utilidad 258); la recta log-log dice 14.0 (utilidad 112). |

Un modelo de caja negra puede recuperar la elasticidad, pero solo si los datos tienen precios que se movieron por razones independientes de la demanda (Parte 3).

El precio óptimo no sale solo de la curva: hay que sumar costo, reglas de la empresa y churn.

Un modelo no sabe lo que no ha visto: antes de usar una predicción hay que revisar que el precio esté dentro del rango con el que se entrenó.

## Entregable

| Qué entregar | Detalle |
| Documento | Esta misma guía, con las respuestas a todas las preguntas escritas en los recuadros "Respuesta del grupo" (una entrega por grupo). |
| Cifras | Incluyan en las respuestas la elasticidad de cada segmento, el precio recomendado con su utilidad esperada, y qué pasó fuera del rango de precios. |
