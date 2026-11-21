# Semana 6 · Técnicas de segmentación de clientes (clase)

(diapositiva 1) Técnicas de Segmentación de Clientes MARKETING ANALYTICS

(diapositiva 5) Lo que tienen en común: distancia y escala DISTANCIA EUCLIDIANA ESTANDARIZAR d(x, y) = √ Σ (xⱼ − yⱼ)² z = (x − μ) / σ Qué tan lejos están dos clientes, sumando la diferencia en cada variable j. Cada variable queda con promedio 0 y desviaciónes por encima dle promedo, para que ninguna domine por tener números grandes. Todas las técnicas parten de la distancia. Lo que cambia es su respuesta a: ¿qué es un grupo?

(diapositiva 7) Cinco respuestas a "¿qué es un grupo?" Técnica Un grupo es… Matemática central k-means Puntos cerca de un centro Minimizar la suma de distancias al cuadrado Jerárquico Lo que se va uniendo por cercanía Matriz de distancias y regla de enlace DBSCAN Una zona densa de puntos Vecindad de radio ε y mínimo de vecinos Mezclas gaussianas Una campana de probabilidad Media, covarianza y peso π de cada campana K-prototypes Como k-means, con categorías Distancia numérica más coincidencia de categorías

(diapositiva 8) k-means: minimizar la dispersión QUÉ MINIMIZA J = Σₖ Σ(x en grupo k) ‖x − μₖ‖² La suma de las distancias al cuadrado entre cada cliente y el centro (μₖ) de su grupo. Asignar Actualizar Repetir Cada cliente va al centro más cercano El centro pasa a ser el promedio de su grupo Hasta que J ya no baja (puede quedar en un mínimo local) Por eso se corre varias veces con centros iniciales distintos y se queda con el menor J.

(diapositiva 9) Ejemplo: k-means con seis clientes Gasto anual en US$: 40, 50, 80, 300, 340 y 420. Queremos k = 2 grupos y partimos de dos centros mal puestos: 40 y 80. Ronda Grupo A Grupo B Centros nuevos J 1 40, 50 80, 300, 340, 420 45 y 285 63,550 2 40, 50, 80 300, 340, 420 56.7 y 353.3 8,333 3 40, 50, 80 300, 340, 420 no cambian 8,333 En la ronda 2 el cliente de 80 se pasa al grupo A: está a 35 del centro 45 y a 205 del centro 285. Con eso J baja de 63,550 a 8,333 y el algoritmo termina.

(diapositiva 10) Por qué k-means siempre ve círculos La distancia mide igual en todas las direcciones. Los puntos a la misma distancia de un centro forman un círculo (una esfera con más variables). La frontera entre dos grupos es una línea recta a mitad de camino entre sus centros. Supone grupos de tamaño parecido y con la misma dispersión en todas direcciones. En términos de probabilidad es el caso Σ = σ² * I de las mezclas gaussianas.

(diapositiva 10) Σ = forma del circulo σ² = varianza I = matriz de identidad (dado que no hay inclinación, produce círculos perfectos)

(diapositiva 11) ¿Cuántos grupos? Dos medidas CODO (INERCIA) SILUETA Se grafica J contra k. J siempre baja al subir k; se busca el punto donde deja de bajar rápido. s = (b − a) / max(a, b) a: distancia media a su propio grupo. b: distancia media al grupo vecino más cercano. Va de −1 a 1. Cerca de 1: bien separado. Cerca de 0: en la frontera. Negativo: probablemente mal asignado. En nuestros datos reales: 0.34 con 2 grupos y 0.25 con 3. Son valores bajos: los grupos no están bien separados.

(diapositiva 12) Ejemplo: la silueta de un cliente Seguimos con los seis clientes. El cliente de US$80 quedó en el grupo A (40, 50, 80). El grupo B es 300, 340, 420. A (SU GRUPO) B (GRUPO VECINO) SILUETA Distancia media a los otros del grupo A: (40 + 30) / 2 = 35 Distancia media a los del grupo B: (220 + 260 + 340) / 3 ≈ 273 s = (273 − 35) / 273 ≈ 0.87: muy bien asignado Si a fuera 150 y b fuera 160, s = (160 − 150) / 160 ≈ 0.06: el cliente está en la frontera y podría pertenecer a cualquiera de los dos grupos.

(diapositiva 13) k-means: usos típicos y variantes Dónde se usa Variantes Segmentar clientes por recencia, frecuencia y gasto (RFM). k-means++: elige los centros iniciales lejos unos de otros, para empezar mejor. Agrupar productos según quién los compra. Mini-batch: usa muestras pequeñas para bases enormes. Comprimir imágenes reduciendo sus colores a k tonos. k-medoids: el centro es un cliente real; funciona mejor con los casos atípicos.

(diapositiva 14) Jerárquico: el enlace decide la forma Parte de la matriz de distancias entre todos los pares y une una y otra vez los dos grupos más cercanos. "Más cercanos" depende de la regla de enlace:

(diapositiva 14) Enlace Distancia entre dos grupos A y B Tiende a formar Simple La menor entre un punto de A y uno de B Cadenas; un ruido puede unir todo Completo La mayor entre un punto de A y uno de B Grupos compactos y parejos Promedio El promedio de todas las parejas Un punto medio entre los dos Ward Cuánto sube la dispersión total al unirlos Grupos redondos, parecido a k-means

(diapositiva 19) El dendrograma y dónde cortar La altura de cada unión es la distancia a la que se juntaron los dos grupos. Un salto grande antes de la siguiente unión indica grupos naturales. Se corta a una altura y quedan los grupos que cruza la línea, sin fijar k de antemano. Límites: guarda la matriz de n × n distancias (muchos clientes pesan), no deshace uniones y depende del enlace y de la escala. La línea naranja es el corte: deja 2 grupos (cuatro clientes a la izquierda y dos a la derecha).

(diapositiva 21) Jerárquico: usos típicos y variantes Dónde se usa Variantes y cuidados Agrupar pocas entidades (países, tiendas, productos) donde importa ver el árbol y no solo los grupos. Aglomerativo: de abajo hacia arriba, el que vimos. Armar jerarquías de productos o categorías. Genética: árboles de parentesco entre especies o muestras. Divisivo: parte de un solo grupo y lo va dividiendo. Cuidado: con decenas de miles de clientes la matriz de distancias se vuelve pesada.

(diapositiva 22) DBSCAN: grupos como zonas densas DOS PARÁMETROS Vecindad: Nε(p) = { q : d(p, q) ≤ ε } , y minPts La vecindad de p son todos los puntos q que están a distancia ε o menos de p Punto núcleo Punto borde Ruido Tiene al menos minPts vecinos a distancia ε o menos No es núcleo, pero está en la vecindad de uno Ni núcleo ni borde: queda sin grupo Un grupo es el conjunto de núcleos que se encadenan por vecindad, más sus bordes. Como se encadena, la forma puede ser cualquiera.

(diapositiva 23) Ejemplo: DBSCAN con nueve clientes Parámetros: ε = 1.5 y minPts = 3 (el propio punto cuenta). Cinco clientes juntos a la izquierda: cuatro son núcleo (tienen 3 o más vecinos dentro del radio) y el de la derecha es borde: solo alcanza a uno de ellos. Tres clientes arriba a la derecha: se tocan entre sí, forman un segundo grupo. El cliente lejano: no tiene vecinos, es ruido. Resultado: 2 grupos y 1 ruido, sin haber dicho cuántos grupos queríamos. Verde y azul: núcleos de cada grupo · Naranja:

(diapositiva 23) borde · Gris hueco: ruido · Círculo punteado: radio ε alrededor de un núcleo

(diapositiva 25) DBSCAN: fortalezas y cuidados Fortalezas Cuidados No necesita fijar k. Un solo ε para todo: falla si los grupos tienen densidades distintas. Encuentra formas irregulares. Separa el ruido en lugar de forzarlo a un grupo. Con muchas variables las distancias se parecen entre sí y la densidad pierde sentido. Muy sensible a ε. Se elige con el gráfico de la distancia al k-ésimo vecino. En nuestros clientes reales:

(diapositiva 25) con ε = 1.5 salen 2 grupos grandes y 143 atípicos; con ε = 2 o más, casi todos quedan en un solo grupo.

(diapositiva 26) DBSCAN: usos típicos y variantes Dónde se usa Cómo ajustarlo Detectar transacciones atípicas, por ejemplo posible fraude. minPts: regla práctica, al menos el número de variables más uno. Encontrar zonas calientes en un mapa: entregas, tiendas, visitas. ε: gráfico de la distancia al k-ésimo vecino, y se busca el codo. Separar a los clientes "raros" para revisarlos aparte. Variante: HDBSCAN no usa un ε único y tolera grupos de densidades distintas.

(diapositiva 27) Mezclas gaussianas: campanas de probabilidad EL MODELO p(x) = Σₖ πₖ · N(x | μₖ, Σₖ) Los datos se ven como una mezcla de k campanas de Gauss, una por grupo. μₖ Σₖ πₖ La media: dónde está el centro de la campana La matriz de covarianza: qué tan ancha es y hacia dónde se inclina El peso: qué fracción de los clientes pertenece al grupo (suman 1)

(diapositiva 28) Ejemplo: un cliente a mitad de camino Dos comportamientos de gasto anual. Un cliente gasta US$250, justo en medio de los dos centros. Grupo Peso π Media μ Desviación σ Distancia de 250 A · gasto bajo 0.70 US$100 US$40 150 B · gasto alto 0.30 US$400 US$150 150 K-MEANS MEZCLA GAUSSIANA Está a la misma distancia de ambos centros: empate. No puede decir más. 1.3% del grupo A y 98.7% del grupo B. El grupo B es mucho más ancho: 250 está a una desviación de B, pero a casi cuatro de A (150 / 40 ≈ 3.75).

(diapositiva 28) La probabilidad pesa la distancia con el ancho de cada campana.

(diapositiva 30) La covarianza convierte el círculo en óvalo La matriz Σ guarda la varianza de cada variable y cuánto se mueven juntas (la covarianza). Sus vectores propios dan la dirección del óvalo y sus valores propios, el largo de cada eje. Si Σ = σ² * I, el óvalo es un círculo: eso es exactamente k-means. Con Σ completa, cada grupo tiene su propio óvalo inclinado.

(diapositiva 31) Cómo aprende: el algoritmo EM PASO E (ESTIMAR) PASO M (MAXIMIZAR) γᵢₖ = πₖ N(xᵢ|μₖ,Σₖ) / Σⱼ πⱼ N(xᵢ|μⱼ,Σⱼ) Recalcular πₖ, μₖ y Σₖ usando esas probabilidades como pesos La probabilidad de que el cliente i pertenezca al grupo k. Se repite hasta que el ajuste a los datos ya no mejora. Asignación suave: un cliente puede ser 70% del grupo A y 30% del B. k-means obliga a elegir uno. Elegir k: con BIC o AIC, que premian el buen ajuste y castigan tener demasiados parámetros. Cuidado:

(diapositiva 31) con Σ completa hay k·d(d+1)/2 parámetros de covarianza; con pocos datos o muchas variables el ajuste se vuelve inestable.

(diapositiva 33) Mezclas gaussianas: usos típicos y cuidados Dónde se usa Cuidados Modelar un gasto que mezcla comportamientos distintos, como compradores ocasionales y frecuentes. Supone que cada grupo es una campana; con colas muy largas o formas raras ajusta mal. Dar un puntaje de pertenencia: "70% comprador de ofertas", útil para campañas graduales. Puede quedar en un óptimo local, así que se corre varias veces. Detectar anomalías: clientes en zonas de muy baja densidad.

(diapositiva 33) Elija k con BIC y compare el resultado con k-means antes de confiar.

(diapositiva 34) K-prototypes: números y categorías juntos COSTO QUE MINIMIZA Σ ‖x numérico − μ‖² + γ · Σ δ(x categórico, moda) δ vale 0 si la categoría coincide con la del centro y 1 si no. γ decide cuánto pesan las categorías frente a los números. Centro del grupo Cuándo sirve Promedio en las variables numéricas y moda (la más frecuente) en las categóricas Datos mixtos: canal, plan, educación o estado civil junto con gasto e ingreso En nuestros datos:

(diapositiva 34) k-prototypes salió casi igual a k-means (acuerdo 0.99), porque el gasto y el ingreso pesan más que la educación o el estado civil.

(diapositiva 35) Ejemplo: el peso γ de las categorías Un cliente y el centro de un grupo, con dos variables numéricas ya estandarizadas y dos categóricas. Variable Cliente Centro Aporte al costo Ingreso (z) 0.9 0.5 0.4² = 0.16 Gasto (z) 1.2 0.1 1.1² = 1.21 Canal Web Tienda δ = 1 (distinto) Plan Premium Premium δ = 0 (igual) γ = 0.5 γ=2 Costo = 1.37 + 0.5 × 1 = 1.87. Las categorías pesan poco: son 0.5 de 1.87. Costo = 1.37 + 2 × 1 = 3.37. Ahora el canal distinto pesa más que el gasto. Variantes:

(diapositiva 35) k-modes (solo categorías) y la distancia de Gower, que permite usar datos mixtos también en el jerárquico.

(diapositiva 37) Las cinco técnicas, lado a lado Técnica Forma del grupo ¿Fijar k? Atípicos Asignación Datos k-means Círculo Sí Lo distorsionan Dura Números Jerárquico Según el enlace Se decide al cortar Depende del enlace Dura Números DBSCAN Cualquiera No Los aparta como ruido Dura o ruido Números GMM Óvalo Sí (BIC) Lo distorsionan Suave Números K-prototypes Círculo Sí Lo distorsionan Dura Mixtos Dura: cada cliente en un solo grupo. Suave: una probabilidad por grupo.

(diapositiva 38) ¿Cuál usar según el escenario? Si su situación es… Pruebe primero Base grande, necesita rapidez y una explicación sencilla k-means Base pequeña y no sabe cuántos grupos hay Jerárquico Hay atípicos o formas irregulares y quiere apartar el ruido DBSCAN Grupos alargados o traslapados, o necesita una probabilidad Mezclas gaussianas Variables numéricas y categóricas mezcladas K-prototypes Lo habitual es probar varias y quedarse con la que mejor sirva para actuar, no solo la de mejor métrica.
