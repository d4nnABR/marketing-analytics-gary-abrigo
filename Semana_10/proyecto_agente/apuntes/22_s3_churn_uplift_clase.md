# Semana 3 · Customer churn y uplift (clase)

(diapositiva 1) Customer Churn • Es el porcentaje de clientes que dejan de usar un producto o servicio en un tiempo fijo. • Se dividen los clientes perdidos entre los clientes que había al inicio, y el resultado se multiplica por 100. • Si tenía 10 clientes al inicio del periodo y perdí 2, tengo una tasa de perdida de: • (2 / 10) * 100 = 20%

(diapositiva 2) Fórmula CLV CLV = (ARPU × margen) × r − CAC (1 + d − r) La tasa multiplicativa: (1 + d - r) • Esta expresión se utiliza en modelos dinámicos o de proyecciones financieras para calcular el factor de cambio de la base de clientes de un período a otro. • Esta fórmula no cuenta cabezas de clientes; sirve para calcular el Valor de Vida del Cliente (Customer Lifetime Value o CLV) a largo plazo. Es decir, ayuda a calcular cuanto dinero dejará un cliente en total antes de que decida irse para siempre.

(diapositiva 3) Impacto de la Perdida o Retención a largo plazo Ejemplo sencillo.. Periodo Número de Clientes iniciales Tasa de Retención Clientes restantes 0 100 95% 95 1 95 95% 90 2 90 95% 86 3 86 95% 82 Dado que el CLV es una métrica a largo plazo, la retención-perdida de clientes debe de analizarse a largo plazo considerando factores tales cómo el valor de dinero en el tiempo, para evaluar el impacto el día de hoy.

(diapositiva 4) Breakout Room # 1 – Palanca “r” vs AOV Diríjase con su grupo a su breakout room, y siga las instrucciones en “breakout_2.ipynb”, una vez terminadas reporte sus resultados de la comparación CLV. Objetivo: • Comparar el valor de aumentar la “Palanca r”, la retención vs. el AOV (Average Order Value) de los clientes. • ¿Quién ganara? • ¿Cuál escenario subió más el CLV, y por cuánto? • ¿Por qué el mismo esfuerzo (+10% en un número, +5 puntos en el otro) produce resultados tan distintos?

(diapositiva 4) • Si tuvieran que elegir UNA iniciativa para el próximo trimestre, una campaña de venta cruzada (sube el AOV) o un programa de retención (sube r), ¿con cuál se van, y por qué, visto el multiplicador?

(diapositiva 5) La retención no es una palanca lineal Cuánto vale un cliente, en meses de margen, según su retención mensual Retención mensual 70% Multiplicador Cambio 2,3× — Subir el AOV promedio un 10% Sube el CLV un 10% AOV = Average Order Value 80% 3,8× +65% 85% 5,3× +39% Subir la retención de 90% a 95% 90% 8,2× +55% Lo sube un 93% 95% 15,8× +93% 97% 24,3× +54% Multiplicador = r / (1 + d − r), con d = 1% mensual

(diapositiva 6) LA PR EGUNTA DE HO Y Si la retención es la palanca más poderosa, ¿cómo la movemos? Y sobre todo: ¿cómo sabemos que la movimos nosotros, y no que esos clientes iban a quedarse igual?

(diapositiva 7) Churn contractual y churn no contractual CONTRACTUAL NO CONTRACTUAL Netflix, el gimnasio, tu operador Starbucks, el supermercado, Amazon El cliente cancela. Hay una fecha, un evento, un registro en la base de datos. El cliente simplemente deja de aparecer. Nadie cancela un café. El churn es un dato que se observa. El churn es algo que se debe definir cuidadosamente Un cliente que lleva 60 días sin venir, ¿se fue o está de viaje? No hay forma de saberlo con certeza. Por eso BG/NBD:

(diapositiva 7) no clasifica vivo o muerto, estima una probabilidad de seguir activo.

(diapositiva 8) Definir el churn es una decisión de negocio No es un parámetro técnico. Cambia a quién se va a contactar y cuánto se va a gastar. Si defines churn como… Clientes marcados Qué te pasa 30 días sin comprar Muchísimos Persigues a gente que solo se fue de vacaciones. Gastas de más. 90 días sin comprar Un número razonable Equilibrio habitual en retail de alta frecuencia. (Starbucks) 180 días sin comprar Pocos Llegas tarde. Cuando lo detectas, ya se fue de verdad.

(diapositiva 8) Definición de Ventana - regla práctica Por segmento, no global La ventana debe ser un múltiplo del ciclo de compra típico. Si nuestros clientes compran cada semana, 90 días son 13 ciclos perdidos: demasiado. Un “Daily Commuter” ausente 14 días ya es alarma. Un “Weekend Commuter” ausente 14 días es normal. Una sola ventana para todos mezcla los dos casos.

(diapositiva 9) Las dos ventanas El error número uno en un modelo de churn es dejar que el futuro se filtre al pasado Ventana de observación Ventana objetivo hoy Aquí se construyen las variables: recencia, frecuencia, gasto, Aquí se mide la etiqueta: ¿volvió o no tendencia, canales. volvió? La fuga de información más común: usar la recencia medida al final de la ventana objetivo. Un cliente que compró ayer obviamente va a comprar:

(diapositiva 9) el modelo da AUC de 0,98 y no sirve para nada, porque en producción esa variable no existe todavía.

(diapositiva 10) Tres familias de modelo Regresión logística Árboles y boosting Predice la probabilidad de churn en la ventana. XGBoost, LightGBM, Gradient Boosting. Pros: los coeficientes se explican a un director. Rápida y estable. Pros: más certeros con datos tabulares. Casi sin preparación. Cons: no captura interacciones sin que se escriban a mano. Cons: caja negra; necesita SHAP para explicarse. Análisis de supervivencia Cox, modelos de hazard, BG/NBD. Pros: responde cuándo, no solo si.

(diapositiva 10) Maneja bien a quien aún no se ha ido. Cons: más difícil de montar y de explicar. Los tres responden la misma pregunta: ¿quién se va a ir? Ninguno responde la que de verdad importa para gastar presupuesto, y eso es lo que vamos a ver ahora.

(diapositiva 11) Cómo se evalúa un modelo de churn El accuracy es inútil aquí, y conviene entender por qué Si el 8% de tus clientes se va, un modelo que diga "no se va nadie" acierta el 92% de las veces. Accuracy 0,92 y cero valor. Métrica Qué responde Cuándo la usas AUC / ROC ¿Ordena bien a los clientes por riesgo? Comparar modelos entre sí Precision@k De los k que marqué, ¿cuántos se fueron de verdad? Cuando el presupuesto solo alcanza para k Recall De los que se fueron, ¿a cuántos detecté?

(diapositiva 11) Cuando perder un cliente es muy caro Lift en el decil 1 ¿Cuántas veces mejor que elegir al azar? Explicárselo a negocio Precision@k es la métrica honesta cuando hay presupuesto limitado, porque obliga a decir cuántos clientes vas a poder contactar antes de medir nada.

(diapositiva 12) Breakout Room # 2 – Calcular el Churn Diríjase con su grupo a su breakout room, y siga las instrucciones, una vez terminadas reporte sus resultados del churn. Objetivo: • Detectar a los clientes que están en riesgo de perderse. • ¿Lograremos retenerlos? • ¿Qué AUC les dio el modelo correcto? ¿Y el que hace trampa? • En una frase: ¿por qué un AUC de 1.0 (o casi) es una mala noticia y no una buena? • Anoten cuántos clientes marcaron como "alto riesgo" (prob > 70%). Vamos a preguntar:

(diapositiva 12) "¿a quién contactamos?“ , con esta lista en la mano, ¿cuál es su respuesta?

(diapositiva 13) HASTA AQUÍ , TOD O BI EN Tenemos un modelo de churn con AUC 0,99. Tenemos presupuesto para contactar al 30%. Contactemos a los de mayor riesgo. Es lo que hace casi todo el mundo. Y es exactamente donde se pierde el dinero.

(diapositiva 14) La pregunta que falta Mandamos la campaña a María. María volvió a comprar. ¿Funcionó? LO QUE VIMOS EN EL MODELO LO QUE NECES ITABAS SABER María recibió la oferta y volvió. ¿Habría vuelto igual sin la oferta? Lo anotamos como una conversión. El reporte dice que la campaña funcionó. Si la respuesta es sí, le regalaste $5 y anotamos un éxito que no existió. Eso que te falta se llama contrafactual Es el mismo cliente, en el mismo momento, sin haber recibido nada. No existe y no se puede observar.

(diapositiva 14) Toda la inferencia causal consiste en construir una aproximación creíble de ese universo paralelo.

(diapositiva 15) Un modelo de churn dice quién se va a ir. Nunca dice a quién se puede retener. Son dos preguntas distintas, y confundirlas cuesta el presupuesto entero.

(diapositiva 16) 4 tipos de clientes 3. Los Perros Dormidos (Sleeping Dogs o Do Not Disturb) Es el grupo más peligroso. Son clientes que están tranquilos o conformes, pero si los contactas, generas el efecto contrario al deseado (se molestan, recuerdan que querían cancelar el servicio o se dan de baja). • Con campaña: No compran (o abandonan la marca). • Sin campaña: Compran (o se quedan quietos pagando el servicio). • Estrategia: Evitarlos a toda costa. El contacto desencadena una respuesta negativa.

(diapositiva 16) Un ejemplo clásico es el cliente que tiene una suscripción olvidada y, al recibir un correo de la empresa, se acuerda de cancelarla.

(diapositiva 17) 4 tipos de clientes 2. Los Persuadibles (Persuadables) Este es el grupo más importante y el verdadero objetivo de cualquier campaña de marketing. Son clientes que solo reaccionarán si se les da un empujón. • Con campaña: Compran. • Sin campaña: No compran. • Estrategia: Concentrar todos los esfuerzos de la campaña en ellos. Aquí es donde la publicidad genera un valor real y un retorno de inversión (ROI) directo, ya que la campaña es la que causa la venta

(diapositiva 18) 4 tipos de clientes 1. Las Causas Perdidas (Lost Causes) Son aquellos clientes que no van a comprar (o renovar) de ninguna manera, independientemente de si reciben la campaña o no. • Con campaña: No compran. • Sin campaña: No compran. • Estrategia: No gastar dinero en ellos. Dirigirles publicidad es un desperdicio de presupuesto porque su respuesta siempre será negativa.

(diapositiva 19) 4 tipos de clientes 4. Una Cosa Segura (Sure Things) Son los clientes que ya están convencidos y van a comprar de todos modos, reciban o no la publicidad. Su lealtad o necesidad actual es alta. • Con campaña: Compran. • Sin campaña: Compran. • Estrategia: No gastar presupuesto de campaña en ellos. Aunque verlos comprar se siente como un éxito, enviarles ofertas o descuentos solo reduce el margen de ganancia de la empresa, ya que habrían pagado el precio completo de igual manera.

(diapositiva 20) Tus clientes son de cuatro tipos SIN campaña: compra SIN campaña: no compra Sure Things Persuadables Iban a comprar igual. Les regalas el descuento. Vuelven solo si los contactas. El único grupo que deja dinero. Uplift 0 · No contactar Uplift positivo · CONTACTAR Sleeping Dogs Lost Causes Compraban, y contactarlos los espanta. Ya se fueron. No hay oferta que los traiga. CON campaña: compra CON campaña:

(diapositiva 20) no compra Uplift 0 · No contactar Uplift NEGATIVO · Jamás contactar Un modelo de churn ve alto riesgo en Lost Causes y en Sleeping Dogs: los dos grupos a los que no hay que escribir

(diapositiva 21) Uplift • En marketing, el uplift (o incremento) es el aumento real en las ventas o en un resultado medible que ocurre gracias a una campaña o acción publicitaria, en comparación con lo que habría pasado sin ella.

(diapositiva 21) • Un cliente puede tener alta probabilidad de comprar y, al mismo tiempo, uplift CERO, porque iba a comprar de todos modos (ese es el "Sure Thing") • También puede tener uplift NEGATIVO , contactarlo reduce su probabilidad de comprar (el "Sleeping Dog") • Entonces uplift no mide "qué tan probable es que compre", mide "qué tan probable es que MI ACCIÓN cambie el resultado"

(diapositiva 22) El uplift de una persona nunca se puede observar. A cada cliente o le mandas la campaña o no se la mandas. El otro resultado pertenece a un universo que no existe, así que no hay etiqueta de uplift que aprender. La salida: no recuperamos el uplift de una persona, sino el de personas como ella. Para eso los dos grupos tienen que ser comparables, y lo único que garantiza eso es el azar.

(diapositiva 23) Experimentar con clientes reales • Si solo miras a tus clientes YA contactados (sin comparar con nadie), no puedes saber si compraron POR el contacto o si iban a comprar de todos modos, estás viendo correlación, no causalidad • La asignación al azar (coin-flip: mitad tratamiento, mitad control) es lo que resuelve esto:

(diapositiva 23) como la asignación es aleatoria, las dos mitades son estadísticamente parecidas en todo lo demás (edad, gasto histórico, lo que sea), la ÚNICA diferencia sistemática entre los dos grupos es si recibieron el contacto o no • Eso permite aproximar el contrafactual de forma indirecta:

(diapositiva 23) en vez de preguntar "¿qué le hubiera pasado a ESTE cliente sin contacto?", preguntas "¿qué le pasó, en promedio, a clientes PARECIDOS que no fueron contactados?" , el grupo de control hace de doble/sustituto • Sin ese grupo de control, no tienes manera de aislar el efecto del contacto de todo lo demás que ya distingue a un cliente que compra de uno que no

(diapositiva 24) Por qué el grupo de control no es opcional Es caro: dejas de contactar a gente que podría comprar. Y aun así es obligatorio. Sin control Con control Contactas a los de más riesgo. El 40% vuelve a comprar. Tratamiento: vuelve el 40%. Control: vuelve el 34%. Reportas: "la campaña recuperó al 40%". Reportas: "la campaña recuperó 6 puntos". No sabes si ese 40% habría vuelto igual. La cifra no significa nada. Esos 6 puntos sí son tuyos. Los otros 34 iban a ocurrir solos. Cuánto control reservar.

(diapositiva 24) Un holdout del 10% basta para medir el efecto promedio. Para modelar uplift hace falta mucho más, nosotros usamos 50/50, porque estimar una diferencia por subgrupo consume una cantidad de datos que sorprende a casi todo el mundo.

(diapositiva 25) Uplift, en una línea uplift(cliente) = P(compra | lo contacto) − P(compra | no lo contacto) No es la probabilidad de que compre. Es cuánto cambia esa probabilidad por haberlo contactado. Modelo de churn Modelo de propensión Modelo de uplift Ordena por riesgo Ordena por probabilidad de responder Ordena por efecto causal Contesta: ¿quién se va? Contesta: ¿quién compra tras la campaña? Contesta: ¿a quién muevo yo? El de propensión también se equivoca:

(diapositiva 25) un Sure Thing tiene altísima probabilidad de comprar tras la campaña, y uplift cero

(diapositiva 26) Tres formas de estimar Uplift S-LEARNER T-LEARNER TRANSFORMACIÓN DE CLASE Un modelo, con el tratamiento como variable Dos modelos, uno por grupo Un truco algebraico Predices dos veces: con tratado=1 y con tratado=0. La diferencia es el uplift. Riesgo: si el modelo decide que esa variable aporta poco, la ignora y el uplift se aplana a cero. Uno aprende de los tratados, otro del control. El del control reconstruye el universo paralelo. Riesgo: los errores de los dos modelos se suman al restar.

(diapositiva 26) Defines Z = 1 si (tratado y compró) o (control y no compró). Entonces uplift = 2·P(Z=1) − 1. Riesgo: exige asignación 50/50, o hay que ponderar. El truco de la transformación de clase convierte un problema causal en una clasificación normal. Z vale 1 justo cuando el cliente se comportó Pros de que la campaña sirva. Lo van a programar en el laboratorio: son cuatro líneas. Lai (2006) y Jaskowski & Jaroszewicz (2012) para la transformación de clase

(diapositiva 27) Breakout Room # 3 – Identificar los 4 cuadrantes Diríjase con su grupo a su breakout room, y siga las instrucciones, una vez terminadas reporte sus resultados del churn. Objetivo: • Detectar a los clientes que están en los cuatro cuadrantes según un experimento de control y tratamiento previo. • Si solo podemos ofrecer descuentos al 30% ¿Lograremos ver en cuales es necesario invertir? • ¿Qué regla dejó más valor incremental total: por riesgo o por uplift?

(diapositiva 27) • .Miren la composición del 30% que targetea "por riesgo" ,¿cuántos Sleeping Dogs se colaron ahí? Eso es exactamente el costo de confundir "en riesgo" con "vale la pena contactar". • Con su propia tabla del Paso 4 en la mano: **¿en qué cuadrante es necesario invertir, y en cuál definitivamente NO?**

(diapositiva 28) Sleeping Dogs: la campaña que ahuyenta El cuadrante que nadie busca porque nadie cree que exista El recordatorio fatal Un correo de "te extrañamos" le recuerda a alguien que lleva meses pagando algo que no usa. Cancela. El cliente premium molesto La fatiga de notificaciones Va poco, gasta bien y le gusta el ritual. Recibir un cupón agresivo le dice que es un número en una base de datos. Un push de más y desactiva las notificaciones, o borra la app. Pierdes el canal para siempre.

(diapositiva 28) En nuestro experimento de Starbucks los Sleeping Dogs son el 4.8% de la base, y contactar a cada uno destruye −$1.48 por cliente

(diapositiva 29) Un modelo de uplift no se evalúa con AUC El AUC mide si acertaste el resultado. Aquí no quieres acertar quién compra: quieres acertar a quién moviste. Y como el uplift verdadero no se observa en nadie, no hay nada contra qué calcular un AUC. Curva Qini Tabla por deciles Valor de la política Si ordeno por uplift predicho y contacto al x% de arriba, ¿cuántas compras incrementales consigo? ¿El uplift real baja de arriba abajo? Si no baja, el modelo no está ordenando nada.

(diapositiva 29) Con esta regla de targeting, ¿cuánto dinero gano o pierdo de verdad? Las tres se calculan comparando tratados contra control dentro de cada grupo, nunca contra una etiqueta de uplift

(diapositiva 30) Coeficiente Qini • Es un solo número que resume "¿qué tan bueno es mi modelo de uplift para ordenar a los clientes?" asi como el AUC resume qué tan bueno es un modelo de churn. • Se construye ordenando a TODOS los clientes de mayor a menor uplift estimado (los que el modelo cree más persuadibles van primero) • Después caminas esa lista de arriba hacia abajo, y en cada punto comparas: de los que ya pasaste, ¿cuántos tratados respondieron vs.

(diapositiva 30) cuántos de control respondieron?, esa diferencia acumulada es la curva Qini • El coeficiente es el ÁREA entre esa curva y la línea de "targeting al azar" (la diagonal), mientras más área, mejor distingue el modelo a los persuadibles de los demás • Un coeficiente Qini alto significa:

(diapositiva 30) "si sigo el orden que me da el modelo, contactar a los primeros de la lista genera mucho más valor incremental que contactar al azar" • Un coeficiente cercano a cero significa que el modelo no está haciendo mejor trabajo que tirar una moneda para decidir a quién contactar

(diapositiva 31) La curva Qini, explicada con manzanas Antes de leer la curva real, construyámosla paso a paso PASO 1 — LA CANASTA MEZCLADA = cliente al que SÍ le diste el descuento (tratado) · al azar, como en el experimento real. = cliente al que NO le diste el descuento (control). Mezclados PASO 2 — EL MODELO LAS REORDENA El modelo de uplift ignora si es o y ordena TODAS las manzanas de "más persuadable" a "menos persuadable".

(diapositiva 31) Las dos primeras manzanas son su apuesta más fuerte, sin importar a qué grupo pertenecen. El orden lo decide el score de uplift predicho, nunca el grupo (tratado o control) al que perteneció cada cliente

(diapositiva 32) Paso 3 — caminas la fila y cuentas En cada punto: de las acumulas. que ya pasaste, ¿qué % compró? De las que ya pasaste, ¿qué % compró? Restas, y Si el modelo no sirve La curva verde cae encima de la diagonal gris. Área ≈ 0. Modelo de uplift área = Qini Al azar (la diagonal) manzanas recorridas, ordenadas por el modelo → La diferencia (% compró entre − % compró entre Si el modelo ordena bien Las primeras manzanas (las más "jugosas") muestran mucha más diferencia vs que las últimas.

(diapositiva 32) La curva se separa de la diagonal. Esa área es el coeficiente Qini. ), acumulada a medida que avanzas, nunca manzana por manzana

(diapositiva 33) Breakout Room # 4 – Qini y Deciles Diríjase con su grupo a su breakout room, y siga las instrucciones, una vez terminadas reporte sus resultados del churn. Objetivo: • Construir la curva Qini y la tabla de deciles para comparar dos formas de ordenar a los 14,000 clientes del experimento , por riesgo/churn y por uplift(T-learner), y ver cuál de las dos sirve de verdad para decidir a quién contactar.

(diapositiva 33) • ¿El coeficiente Qini del modelo de riesgo/churn es mayor, menor o parecido al del modelo de uplift? ¿Qué dice eso sobre usar un modelo de churn para decidir a quién contactar? • Miren la tabla de deciles: ¿hay algún decil donde lo predicho y lo real se alejan mucho? Con ~420 clientes por decil, ¿qué tan confiables son esos números? • Si tuvieran que explicarle a alguien de negocio qué es el coeficiente Qini en una frase, ¿qué dirían?

(diapositiva 34) La curva Qini del experimento Compras incrementales acumuladas según a qué porcentaje de la base contactes Coeficiente Qini · uplift Presupuesto para el 30% 0.222 Coeficiente Qini · churn +0.006 Cero es repartir al azar. Negativo significa ordenar al revés: contactar primero a los peores.

(diapositiva 35) ¿El modelo ordena de verdad? Deciles por uplift predicho, contra el uplift real medido comparando tratados y control dentro de cada decil Decil Uplift predicho Uplift real 1 (mejor) +0,223 +0,188 2 +0,151 +0,170 3 +0,110 +0,091 4 +0,078 +0,100 5 +0,055 +0,033 6 +0,039 −0,045 7 +0,023 +0,027 8 +0,008 +0,040 9 −0,007 −0,002 10 (peor) −0,056 −0,004 Los tres primeros deciles Predicho y real coinciden de cerca. Ahí están los Persuadables, y ahí va el presupuesto.

(diapositiva 35) El decil 6 se sale del patrón Predice +0,039 y mide −0,045. No lo escondas: con 1.400 clientes por decil, el intervalo de confianza es ancho. Una escalera perfecta sería motivo de sospecha, no de celebración. T-learner · 14.000 clientes de prueba

(diapositiva 36) Conclusiones finales El experimento: Starbucks Rewards Campaña de reactivación con asignación aleatoria. Base de clientes La oferta Ventana de medición 40,000 $5 60 días Mitad tratamiento, mitad control Push con descuento en la próxima compra ¿Volvió a comprar? ¿Cuánto gastó? La economía de contactar a un cliente valor = uplift × margen si vuelve − $5 × P(vuelve | tratado) − $0,05 de envío El término naranja es la clave: el descuento se paga también a quien iba a comprar de todos modos.

(diapositiva 36) Esa es la cannibalización que ningún modelo de churn ve.

(diapositiva 37) Caso Hipotetico – Contactemos a todos… Grupo tratamiento Grupo control Efecto promedio 63.3% 56.8% +6.5 pp volvió a comprar volvió a comprar estadísticamente sólido "La campaña funcionó. Subió la retención 6.5 puntos. Lancémosla a toda la base."

(diapositiva 38) Lo que ese +6,5% esconde La composición real de la base. En la vida real es invisible; aquí la conocemos porque los datos son simulados. Tipo de cliente % base Uplift real Valor de contactarlo Sure Things 48,1% +0,004 −$4,73 Persuadables 22,7% +0,287 +$7,91 Lost Causes 22,0% +0,018 +$0,13 Sleeping Dogs 7,1% −0,163 −$5,76 Casi la mitad de la base Solo un grupo deja dinero destruye valor al ser contactada y es el 22,7%

(diapositiva 39) Ejemplos Reales Banco anonimo en USA Resultados https://tdwi.org/articles/2007/10/18/case-study-top-retail-bank-more-than-doubles-campaign-profitability-using-latest-umt.aspx

(diapositiva 40) Ejemplos Reales Consultoría https://cmr.berkeley.edu/2025/11/to-treat-or-not-totreat-five-lessons-learned-from-using-upliftmodeling-to-optimize-marketing-campaigns/

(diapositiva 41) Ejemplos Reales Uber Uber: experimento de promoción para adoptar un producto nuevo Un experimento con un grupo de control y dos de tratamiento (600K observaciones de entrenamiento, 800K de prueba, 139 variables). Conversión de 0.53% en control, 1.39% en el tratamiento 1 y 2.18% en el tratamiento 2. Los modelos que optimizan valor neto (descontando el costo de la promoción) superaron a los modelos estándar y a los grupos originales del experimento. https://arxiv.org/abs/1908.05372

(diapositiva 42) Conclusiones El costo oculto de dar descuento a todos El descuento a todos tiene tres costos que no salen en el reporte de conversión: • Pagas el cupón a los Sure Things, que habrían comprado igual. • Provocas efecto negativo en los Sleeping Dogs. • Acostumbras al cliente a esperar la promoción. Los casos reales lo muestran.

(diapositiva 42) En el retailer del artículo de California Management Review, contactar a todos subió la conversión (15.07% → 18.04%) pero bajó la utilidad por cliente por debajo del control ($5.26 → $5.18). El targeting por uplift la subió a $5.46.

(diapositiva 43) Conclusiones Cómo medir el éxito de verdad Una campaña no se mide por cuántos compraron, sino por cuántos compraron por la campaña. Eso exige un grupo de control aleatorio, porque nadie observa el contrafactual. Mide en tres capas: • Incrementalidad: la diferencia entre tratamiento y control, no solo la tasa de respuesta. • Valor neto: margen incremental menos costo del cupón y del envío. • Calidad del ranking: AUC y Precision@k para churn; Qini para uplift.

(diapositiva 43) Una campaña con buena conversión puede perder dinero.

(diapositiva 44) Conclusiones La ética de a quién le damos el descuento Efectos del Uplift reales: • El uplift tiende a no dar descuento al cliente fiel (Sure Thing), porque ya compra. Es eficiente, pero esa persona paga precio completo mientras otro recibe oferta. • Si el criterio es sensible al cliente que amenaza con irse, puede incentivar ese comportamiento. • Una salida razonable es combinar el uplift con reglas explícitas:

(diapositiva 44) recompensas de lealtad visibles, topes de uso, y un porcentaje de control que no se toca.

(diapositiva 45) Conclusiones Churn y calidad de servicio • El modelo de churn te dice quién se va, pero no por qué. Muchas veces la causa es una mala experiencia, y un descuento no la arregla. • Un cliente molesto por un mal servicio quizá necesita una solución, no un cupón. • Cuando sea posible, conviene cruzar el riesgo de churn con indicadores de servicio (satisfacción, tiempos de resolución, reclamos repetidos) para entender las causas de la salida.

(diapositiva 45) La correlación indica dónde mirar, pero para confirmar que mejorar el servicio reduce el churn hay que probarlo con un experimento con grupo de control.
