# Semana 4 · Venta cruzada y sistemas de recomendación (clase)

(diapositiva 1) Venta Cruzada y Sistemas de Recomendación MARKETING ANALYTICS

(diapositiva 2) Cómo va a ser la sesión Un poco de teoría. un breakout; así cuatro veces SLIDES BREAKOUT ROOMS 0–30 · Apertura y Apriori 30–55 · 1. Apriori: qué se compra junto 65–75 · La matriz y la similitud 75–95 · 2. Matriz y similitud 95–110 · Filtrado colaborativo 110–140 · 3. Recomendar: por ítem y por cliente 140–150 · Cómo medir 150–170 · 4. Comparar y medir 170–180 · Cierre 55–65 · Descanso

(diapositiva 3) La fórmula del CLV tiene tres palancas Ya movimos una. Hoy movemos la segunda. CLV = (ARPU × margen) × r / (1 + d − r) − CAC YA LO VIMOS HOY APARTE Retención (r) ARPU CAC Churn y uplift: cuánto se queda el cliente y a quién conviene contactar. Venta cruzada y recomendación: cuánto nos deja cada cliente. Lo que cuesta traer al cliente. Se resta una sola vez. Esta sesión sube el valor por cliente sin necesitar más clientes

(diapositiva 4) El ARPU es una palanca lineal La retención se dispara; el ARPU sube parejo RETENCIÓN: NO ES LINEAL ARPU: ES LINEAL 8.2× → 15.8× +10% → +10% Subir la retención de 90% a 95% casi duplica el multiplicador del CLV. 10% más de ARPU es 10% más de ingreso por cliente: ni más ni menos. Las dos palancas se combinan. Hoy aprendemos a mover la segunda: ofrecer lo que el cliente probablemente quiere y todavía no compró.

(diapositiva 6) Valor vs. Factibilidad • Los sistemas de recomendación que permiten mejorar el CrossSelling y Upselling son una de las iniciativas más utilizadas en AI por sus atributos que permiten aumentar el valor de consume por transacción promedio de los clientes.

(diapositiva 7) Personalizar no es gratis ni siempre bien recibido Tres cifras de Gartner para tener presentes 53% 38% 80% de los clientes vive experiencias negativas con marketing personalizado. y esos clientes se arrepienten de la compra 3.2 veces más. dejaría de hacer negocios con una empresa si su personalización le parece "creepy". de los marketers que invirtieron en personalización la abandonaría para 2025 por falta de ROI o por problemas de datos. 1.464 personas. 2025 Más de 2.500 clientes.

(diapositiva 7) 2019 Predicción de 2019; el plazo ya pasó Fuente: Gartner. comunicados de prensa (2019. 2025). Ninguna cifra mide el aumento de ARPU por venta cruzada.

(diapositiva 8) La canasta: qué se compra junto Cada orden es una canasta. Una regla A → B dice: quien lleva A. suele llevar B. Canasta 1 Canasta 2 Canasta 3 Canasta 4 Latte Americano Frappuccino Latte Croissant Sándwich Galleta Croissant Agua En nuestros datos hay 14.579 órdenes de 2.000 clientes. con 29 productos y 2.01 productos por orden. Agua Pregunta: si alguien compra Latte. ¿compra Croissant? Y. ¿es eso más que casualidad?

(diapositiva 9) ¿Qué es Apriori y por qué se llama así? Un algoritmo para encontrar qué se compra junto. sin contar todas las combinaciones E L NO M B RE "A priori" = "de antemano" Viene del latín: lo que se sabe antes de mirar los datos. Apriori usa una verdad que se sabe de antemano: si una combinación es rara. cualquier combinación más grande que la incluye es todavía más rara. Si Fresa + Crema casi no aparece. Fresa + Crema + Queso aparece menos aún. No hace falta ni contarla. QUÉ HACE. EN TRES PASOS 1.

(diapositiva 9) Cuenta qué productos y combinaciones aparecen en suficientes canastas (el soporte mínimo). 2. Descarta de antemano lo raro. y todo lo que lo contiene. 3. Con lo que sobrevive arma reglas A → B y las mide con confianza y lift. Es como un mesero que deja de ofrecer los combos que nadie pide. para no revisar todas las combinaciones posibles. Algoritmo de Agrawal y Srikant (1994) · En Python: mlxtend. función apriori

(diapositiva 10) Las tres fórmulas. en preguntas simples A es lo que ya lleva el cliente; B es lo que podríamos ofrecerle SOPORTE CONFIANZA LIFT canastas con A y B canastas con A y B confianza(A → B) todas las canastas canastas con A % de canastas con B ¿Qué tan común es esta pareja? Si lleva A. ¿qué tan seguido lleva también B? ¿Lleva B por llevar A. o lo habría llevado igual? Cuenta cuántas canastas llevan los dos y divide entre el total. Un soporte bajo es una pareja rara.

(diapositiva 10) Mira solo las canastas con A y pregunta qué parte lleva B. Es la probabilidad de B sabiendo A. Compara la confianza con lo normal. Descuenta los productos que van en todas las canastas. Cómo leer el lift: 1 = A no cambia nada · mayor que 1 = se compran juntos más de lo normal · menor que 1 = se evitan. En símbolos: confianza = P(B | A) · lift = P(B | A) ÷ P(B)

(diapositiva 11) Ejemplo a mano (1 de 2): contar Una frutería con 10 canastas; todo se reduce a contar LAS 10 CANASTAS PASO 1: CONTAR 1. Fresa. Crema. Plátano 6. Plátano Total de canastas: 10 2. Fresa. Crema 7. Plátano. Manzana Con Fresa: 4 3. Fresa. Plátano 8. Fresa. Crema. Plátano 4. Manzana. Canela. Plátano 9. Plátano Con Fresa y Crema: 3 10. Manzana. Canela Con Fresa y Plátano: 3 Con Crema: 3 Con Plátano: 7 5. Manzana. Canela Dos reglas con la misma Fresa: Fresa → Crema y Fresa → Plátano.

(diapositiva 11) ¿Cuál vale la pena ofrecer?

(diapositiva 12) Ejemplo a mano (2 de 2): calcular FR E SA → CR E M A FR E SA → P LÁT AN O Soporte = 3 ÷ 10 = 30% Soporte = 3 ÷ 10 = 30% Confianza = 3 ÷ 4 = 75% Confianza = 3 ÷ 4 = 75% Crema en todas las canastas = 3 de 10 = 30% Plátano en todas las canastas = 7 de 10 = 70% Lift = 75% ÷ 30% Lift = 75% ÷ 70% 2.5 1.07 Quien lleva Fresa lleva Crema 2.5 veces más seguido que el promedio. Casi igual que el promedio: el Plátano iba a ir de todos modos. Las dos reglas tienen la misma confianza (75%).

(diapositiva 12) pero solo una vende algo que no se habría vendido solo. Eso es lo que revela el lift.

(diapositiva 13) B R E A KO U T R O O M 1 · 2 5 M I N Apriori: qué se compra junto Qué van a hacer Preguntas 1. Calcular a mano soporte. confianza y lift de Latte → Croissant (TODO 1). 1. ¿Por qué X → Agua tiene confianza alta y lift cerca de 1? 2. Correr Apriori y quedarse con las reglas buenas: confianza ≥ 0.25 y lift ≥ 1.5 (TODO 2). 2. ¿El lift más alto es la oferta que más margen deja? 3. Descubrir la trampa del Agua. 3. ¿En qué dirección harían la oferta en caja? 4. Decidir qué oferta hacer en caja.

(diapositiva 14) Tres números para cada regla Ejemplo real de la base: Latte → Croissant SOPORTE CONFIANZA LIFT 2.9% 32% 6.0 Latte y Croissant juntos aparecen en el 2.9% de todas las canastas. De las canastas que llevan Latte. el 32% también lleva Croissant. 32% ÷ 5.4% (lo normal) = 6. Quien compra Latte lleva Croissant 6 veces más seguido que el promedio. Lift = confianza ÷ % de canastas que llevan B. Lift mayor que 1: se compran juntos más de lo normal. Lift cerca de 1: no hay relación.

(diapositiva 15) La trampa: confianza alta y lift cerca de 1 La confianza sola premia lo que ya es popular PARECE BUENA. NO LO ES REGLA DE VERDAD Muffin → Agua Granola → Matcha Latte Confianza 48% · Lift 1.04 Confianza 58% · Lift 7.9 Banana Bread → Agua Sándwich → Americano Confianza 48% · Lift 1.03 Confianza 50% · Lift 6.9 El Agua va en el 46% de todas las canastas. Entonces casi cualquier producto "predice" Agua con confianza cercana a 46%.

(diapositiva 15) Ofrecerla no vende nada que no se hubiera vendido igual, o algo que no se vendiera sin la recomendación. En otras palabras ofrecer agua seria causar ruido innecesario.

(diapositiva 16) La matriz cliente × producto Una fila por cliente. una columna por producto; 1 = lo compró Latte Croissant Ensalada Americano Ana 1 1 0 0 Beto 1 1 0 1 Carla 0 0 1 0 Diego 0 0 1 1 En nuestros datos: 2.000 clientes × 29 productos. Solo el 14.2% de las celdas tiene un 1. El 85.8% está vacío. 268 clientes no compraron nada antes del corte: no hay nada que comparar. Dos clientes se parecen si sus filas se parecen. Dos productos se parecen si sus columnas se parecen.

(diapositiva 16) Ejemplo ilustrativo de 4 clientes; los totales son de la base completa

(diapositiva 17) Paso 1: el producto punto a · b = multiplicar posición por posición y sumar; da un solo número ANA (A) Y BETO (B) CÓMO SE HACE Latte Croissant Ensalada Americano a (Ana) 1 1 0 0 b (Beto) 1 1 0 1 a×b 1 1 0 0 a·b=1+1+0+0=2 1. Multiplica posición por posición: primero con primero, segundo con segundo… 2. Suma todos los resultados. Resultado: un solo número, no otro vector. Con 0 y 1, solo el 1 × 1 vale 1: el producto punto cuenta cuántos productos compraron los dos. Todavía no alcanza para comparar:

(diapositiva 17) el producto punto crece con la cantidad de productos que compra cada cliente. Falta corregir por tamaño.

(diapositiva 18) Paso 2: la norma, el largo del vector |a| = √(a₁² + a₂² + … + aₙ²): elevar al cuadrado, sumar y sacar la raíz EL LARGO DE CADA CLIENTE POR QUÉ DIVIDIR Ana [1, 1, 0, 0] Ana comparte 2 productos con Beto y 2 productos con el Cliente grande: empate en el producto punto. 1² + 1² + 0² + 0² = 2 → |a| = √2 ≈ 1,41 Beto [1, 1, 0, 1] 1² + 1² + 0² + 1² = 3 → |b| = √3 ≈ 1,73 Pero el Cliente grande compró de todo y "se parece" a cualquiera. Dividir entre los largos corrige eso:

(diapositiva 18) Cliente grande [1, 1, 1, 1] 1 + 1 + 1 + 1 = 4 → |g| = √4 = 2 Ana y Beto: 2 ÷ (1,41 × 1,73) = 0,82 Con 0 y 1: |a| = √(cantidad de productos que compró). Ana y Cliente grande: 2 ÷ (1,41 × 2) = 0,71 |a| × |b| es una multiplicación normal de dos números (el largo de a por el largo de b). No es una multiplicación de vectores. La norma |a| también se escribe ‖a‖ · En numpy: np.linalg.norm(a)

(diapositiva 19) Juntando todo: la similitud coseno similitud(a, b) = a · b ÷ (|a| × |b|) ANA Y BETO, PASO A PASO ANA COMPARADA CON… 1. a · b = 2 Beto [1, 1, 0, 1] 0,82 2. |a| = √2 ≈ 1,41 y |b| = √3 ≈ 1,73 Cliente grande [1, 1, 1, 1] 0,71 3. |a| × |b| ≈ 1,41 × 1,73 ≈ 2,45 Carla [0, 0, 1, 0] 0,00 4. similitud = 2 ÷ 2,45 ≈ 0,82 Diego [0, 0, 1, 1] 0,00 Es el coseno del ángulo entre los dos vectores: 1 = misma dirección (0°), 0 = nada en común (90°). Ana y Beto forman unos 35°.

(diapositiva 19) Para productos es el mismo cálculo con columnas: cosine_similarity(X) compara clientes y cosine_similarity(X.T) compara productos

(diapositiva 21) Ejemplo a mano (1 de 2):

(diapositiva 21) el parecido entre productos Seis clientes, cuatro productos; se comparan las columnas PARECIDO ENTRE COLUMNAS QUIÉN COMPRÓ QUÉ Latte Croissant Ensalada Té Ana 1 1 0 0 Beto 1 1 0 1 Carla 0 0 1 Diego 0 0 Elena 1 Fabio Compran Latte – Croissant 3 ÷ √(4 × 3) 0,87 Latte – Ensalada 1 ÷ √(4 × 3) 0,29 1 Latte – Té 1 ÷ √(4 × 2) 0,35 1 0 0 ÷ √(3 × 3) 0,00 0 1 0 Croissant – Ensalada 1 1 0 0 Croissant – Té 1 ÷ √(3 × 2) 0,41 4 3 3 2 Ensalada – Té 1 ÷ √(3 × 2) 0,41 Ejemplo, Latte – Croissant:

(diapositiva 21) 3 clientes compraron los dos (Ana, Beto, Fabio); Latte tiene 4 compradores y Croissant 3. Se parecen mucho: 0,87. La fórmula es la de la slide anterior; con compras de sí o no, el coseno se reduce a esta cuenta

(diapositiva 22) Ejemplo a mano (2 de 2): qué le recomendamos a Elena Cada producto que ya compró vota por los parecidos ELENA YA COMPRÓ: LATTE Y ENSALADA LE RECOMENDAMOS Croissant = sim(Latte, Croissant) + sim(Ensalada, Croissant) = 0,87 + 0,00 = 0,87 1. Croissant Té = sim(Latte, Té) + sim(Ensalada, Té) = 0,35 + 0,41 = 0,76 porque compraste Latte 2. Té porque compraste Latte y Ensalada Latte y Ensalada no se evalúan: Elena ya los tiene. Mira el Té:

(diapositiva 22) sumar dos parecidos débiles (0,35 + 0,41) casi iguala a un parecido fuerte (0,87). Cada producto que el cliente tiene agrega votos.

(diapositiva 24) B R E A KO U T R O O M 2 · 2 0 M I N La matriz y la similitud Qué van a hacer Preguntas 1. Mirar la matriz de 2.000 clientes × 29 productos (ya armada). 1. ¿Qué bloques ven en el mapa? ¿Qué clientes representan? 2. Calcular la similitud entre los clientes 14. 1015 y 62 (TODO 1). 2. ¿Qué pasa con el Agua y por qué? 3. Calcular la similitud entre productos (TODO 2). 4. ¿Qué pasa con 10.000 productos y 2 millones de clientes? 4. Leer el mapa de calor y ver quién no tiene historia. 3.

(diapositiva 24) ¿Qué le recomendarían a un cliente sin historia?

(diapositiva 25) Qué tan parecidos son dos clientes o dos productos Similitud coseno: de 0 (no comparten nada) a 1 (idénticos) similitud(a. b) = a · b / (|a| × |b|) Cliente 14 y cliente 1015 0.83 Comparten 5 de sus 6 productos. Cliente 14 y cliente 62 Latte y Croissant Latte y Ensalada 0.00 0.51 0.06 No comparten ningún producto. Los compran los mismos clientes. Casi nadie compra ambos. Ojo con el Agua: casi todos la compran. así que se parece a todo y no distingue a nadie. Se excluye antes de recomendar.

(diapositiva 25) Cifras de los notebooks del Breakout 2

(diapositiva 26) Filtrado colaborativo: dos caminos La misma matriz. mirada por columnas o por filas POR ÍTEM POR CLIENTE "Porque compraste X" "Los que se parecen a ti compraron" Pregunta: a quien ya compró estos productos. ¿qué otros productos se parecen a ellos? Pregunta: ¿qué compraron los clientes más parecidos a mí que yo todavía no he comprado? Puntaje de un candidato = suma de su similitud con cada producto que el cliente ya tiene. Puntaje de un candidato = lo que compraron los 30 vecinos más parecidos.

(diapositiva 26) ponderado por su similitud. En los dos casos se excluye lo que el cliente ya compró. y se ordena por puntaje para recomendar los 3 mejores.

(diapositiva 27) Por ítem: "porque compraste X" Ejemplo con el cliente 14 LO QUE YA COMPRÓ LE RECOMENDAMOS Cappuccino. Flat White. Muffin. Té Chai y Banana 1. Té Verde Bread 2. Croissant 3. Latte ¿Por qué Té Verde? Se parece a lo que ya compró: a Té Chai (0.58) y a Banana Bread (0.52). Cada recomendación se puede explicar con "porque compraste X". El Agua no se recomienda: ya vimos que no distingue a nadie

(diapositiva 28) Por cliente: "los que se parecen a ti compraron" El mismo cliente 14. ahora con sus vecinos PASO 1 PASO 2 RESULTADO Buscar 30 vecinos Sumar lo que compraron Té Verde. Croissant. Galleta Cada producto suma la similitud de los vecinos que lo compraron. Té Verde lo compraron 10 de los 30 vecinos. Los 30 clientes con filas más parecidas a la del cliente 14 (similitud coseno). Los dos métodos coinciden en la recomendación #1 para el 68% de los clientes con historia.

(diapositiva 28) Y en al menos 2 de las 3 primeras para el 82%. Casi lo mismo. a distinto costo.

(diapositiva 29) Por qué la similitud entre productos escala mejor El catálogo cambia lento; los clientes cambian a diario PRODUCTO × PRODUCTO CLIENTE × CLIENTE 841 celdas 4.000.000 celdas Aquí: 29 × 29. Con 10.000 productos: 100 millones. Se calcula una vez y se guarda. Aquí: 2.000 × 2.000. Con 2 millones de clientes: 4 billones. Y cambia con cada cliente nuevo. Por ítem: estable. barato y explicable. Es la idea que popularizó Amazon. Por cliente: capta gustos de nicho. pero cuesta más y es más inestable.

(diapositiva 29) Referencia: Linden. Smith y York (2003). Amazon.com Recommendations: Item-to-Item Collaborative Filtering

(diapositiva 32) B R E A KO U T R O O M 3 · 3 0 M I N Recomendar: por ítem y por cliente Qué van a hacer Preguntas 1. Puntaje por ítem: producto punto entre el cliente y la similitud de productos (TODO 1). 1. ¿Recomiendan lo mismo? ¿Cuándo preferirían cada uno? 2. Puntaje por cliente: suma ponderada de los 30 vecinos (TODO 2). 2. Con 2 millones de clientes y 10.000 productos. ¿qué matriz guardarían de antemano? 3. Explicar la primera recomendación de cada método. 3.

(diapositiva 32) ¿Qué hacen con un cliente sin historia y con un producto nuevo? 4. Comparar coincidencia. tiempos y casos sin historia. 4. ¿Cómo sabrían cuál recomienda mejor?

(diapositiva 35) Medir como en BG/NBD: esconder el futuro El mismo corte de siempre: 1 de junio de 2026 Entrenamiento Holdout: 90 días Todo hasta el corte. De aquí salen la matriz. las reglas y las similitudes. Lo que el cliente probó después. escondido. La respuesta del examen: los productos nuevos que el cliente probó en el holdout. que nunca había comprado antes. 986 de 2.000 clientes (49%) probaron algún producto nuevo en esos 90 días. Regla de oro:

(diapositiva 35) nada de lo que pasó después del corte puede usarse para armar el recomendador.

(diapositiva 36) Tres métricas para un recomendador Recomendamos 3 productos a cada cliente y miramos qué pasó HIT RATE@3 PRECISIÓN@3 COBERTURA De los clientes que probaron algo nuevo. ¿en qué porcentaje al menos una de las 3 recomendaciones fue acierto? De las 3 recomendaciones. ¿qué fracción fueron aciertos. en promedio? ¿Cuántos productos distintos del catálogo recomienda el método a alguien? (de 28) Los 4 métodos: popularidad (lo más comprado. igual para todos). Apriori.

(diapositiva 36) filtrado por ítem y filtrado por cliente. La popularidad es la línea base: si un método complejo no le gana. no vale la pena. Se excluye lo que el cliente ya compró y el Agua de las recomendaciones

(diapositiva 37) B R E A KO U T R O O M 4 · 2 0 M I N Comparar los métodos y medir Qué van a hacer Preguntas 1. Ver el holdout y los cuatro recomendadores (ya armados). 1. ¿Qué método llevarían a producción y por qué? 2. Completar el hit rate@3 (TODO 1) y la cobertura (TODO 2). 2. Un directivo dice "acertó 70%. subió el ARPU 70%". ¿Qué le contestan? 3. Comparar los métodos contra la popularidad. 3. Diseñen en tres líneas el experimento para medir el ARPU incremental. 4. Discutir qué significa para el ARPU. 4.

(diapositiva 37) ¿Qué riesgos de "creepy" o de sesgo ven?

(diapositiva 38) ¿Le ganamos a lo simple? Hit rate@3 de los cuatro métodos en el holdout de 90 días 34.7% 58.6% 56.4% 40.9% Popularidad Apriori Por ítem Por cliente cubre 13 de 28 cubre 19 de 28 cubre 28 de 28 cubre 28 de 28 El filtrado por ítem le gana a la popularidad por 69% en términos relativos. y recomienda todo el catálogo. Apriori queda en medio: sus reglas son iguales para todos y solo cubren los pares fuertes.

(diapositiva 39) Acertar no es lo mismo que causar El puente con uplift: ¿cuánto ARPU agrega de verdad el recomendador? LO QUE MEDIMOS LO QUE NECESITAMOS ¿El cliente probó el producto que le recomendamos? ¿Lo probó porque se lo recomendamos? Efecto en ARPU ≈ (tasa con recomendación − tasa sin) × precio × margen En el holdout nadie recibió recomendaciones. y aun así el 49% de los clientes probó algo nuevo. Hace falta un grupo de control aleatorio: es la misma resta de las clases de uplift.

(diapositiva 40) ¿Cuándo recomendar deja de ayudar? Cuatro riesgos que no aparecen en el hit rate Burbuja de popularidad Cliente encasillado Todos reciben lo mismo. La popularidad cubrió 13 de 28 productos; el catálogo largo nunca se muestra. Recomendar solo lo parecido a lo que ya compró encierra al cliente en su gusto. Datos sensibles "Creepy" Las compras pueden revelar cosas que el cliente no contó. No todo lo que se puede inferir se debe usar. Ofertas que parecen adivinar demasiado. Según Gartner (2019).

(diapositiva 40) 38% dejaría de hacer negocios con la empresa.

(diapositiva 41) Completamos la fórmula CLV = (ARPU × margen) × r / (1 + d − r) − CAC RETENCIÓN ARPU · HOY SIGUIENTE Churn y uplift Apriori y filtrado colaborativo Caso ¿Quién se va. y a quién conviene contactar? ¿Qué ofrecerle a cada cliente. y cómo saber si funciona? Aplicar todo junto a un caso real. Para llevarse: un recomendador se mide con holdout. se compara contra lo simple. y su efecto real en ARPU solo se conoce con un grupo de control.
