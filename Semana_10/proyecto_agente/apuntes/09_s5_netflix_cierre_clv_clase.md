# Semana 5 · Netflix, recomendación y cierre de CLV (clase)

(diapositiva 1) Netflix, Recomendación y cierre de CLV MARKETING ANALYTICS

(diapositiva 2) La fórmula completa Cada palanca la movimos con una herramienta distinta. Hoy las comparamos. CLV = (ARPU × margen) × r / (1 + d − r) − CAC MARGEN RETENCIÓN ARPU CAC Precio y costo Churn y uplift Recomendación Adquisición Lo que Netflix cobra y lo que gasta en contenido por miembro. Cuánto se queda el cliente y a quién conviene contactar. Qué mostrarle a cada cliente para que vea más y se quede. Lo que cuesta traer un cliente, y cuánto habría llegado igual.

(diapositiva 4) Lo que Netflix reporta de verdad Reportes anuales (10-K) de 2017 a 2019. Con esto sale el margen por miembro. Dato 2017 2018 2019 Ingresos (US$ millones) 11,693 15,794 20,156 Marketing (US$ millones) 1,436 2,369 2,652 Miembros pagos al cierre (millones) 110.6 139.3 167.1 Altas netas (millones) 21.6 28.6 27.8 Margen mensual por miembro (US$) 3.07 3.90 4.20 El margen sube de US$3.07 a US$4.20 en dos años, aunque Netflix gasta cada vez más en contenido:

(diapositiva 4) el ingreso por miembro crece más rápido que el costo. Fuente: formularios 10-K de Netflix. Margen = (ingresos − costo de ingresos) ÷ miembros promedio ÷ 12

(diapositiva 5) El CAC de Netflix, con y sin las bajas Mismo gasto de marketing, dos denominadores distintos. CAC APARENTE CAC CON BAJAS (CHURN SUPUESTO 2.5%) US$95 US$36 2,652 ÷ 27.8 millones de altas netas. Ignora a quienes cancelaron y fueron reemplazados. 2,652 ÷ 73.7 millones de altas brutas = altas netas + (miembros promedio × churn × 12.) Churn mensual supuesto CAC CLV CLV / CAC 2.0% US$41 US$147 3.58 2.5% US$36 US$124 3.45 3.0% US$32 US$107 3.35

(diapositiva 7) ¿Qué palanca mueve más la razón CLV/CAC? Punto de partida: 3.45 CLV mas que CAC. Cada barra cambia una sola palanca. Ingreso por miembro ±10% 2.55 – 4.35 Churn ∓0.5 pt 2.98 – 4.08 Descuento ±0.4 pt 3.07 – 3.92 CAC ∓10% 3.13 – 3.83 Costo por miembro ∓5% 3.17 – 3.73 Peor Mejor El precio es la palanca más fuerte sobre el papel, pero es la que más reacciona en contra: subir el precio también puede subir el churn.

(diapositiva 8) Subir el precio contra recomendar mejor Dos formas de ganar más por cliente, con distinto riesgo. HOY US$124 CLV por miembro, razón 3.45, recuperación en 8.6 meses. PRECIO +10%, CHURN +0.5 PT MEJOR RECOMENDACIÓN, CHURN −0.5 PT US$135 US$147 +9% de CLV. Si el churn sube más de 0.8 pt (a 3.3%), el aumento ya destruye valor. +18% de CLV sin cobrar más. Su riesgo es que el efecto no sea tan grande como se supone. Para decidir:

(diapositiva 8) ¿cuánto churn adicional tolera el aumento de precio, y cuánto churn quita de verdad la recomendación? Ninguna de las dos respuestas está en el 10-K.

(diapositiva 9) Por qué Netflix recomienda: retención La cadena que usa el caso y que Netflix defendió con datos propios. 1 2 3 4 Recomendar Encontrar rápido Quedarse CLV más alto Mostrar lo que probablemente le gusta. Menos tiempo buscando, más tiempo viendo. Menos cancelaciones mes a mes. Retención entra en el denominador de la fórmula.

(diapositiva 9) Según Gomez-Uribe y Hunt (2015), los dos ejecutivos que dirigían el producto, la recomendación y la personalización reducen la cancelación y le ahorran a Netflix más de mil millones de dólares al año, y la gran mayoría de las horas vistas empieza en algo que el sistema sugirió. Es una cifra que Netflix reporta de sí misma, no una auditoría externa. Por eso importa medirlo con un experimento. Gomez-Uribe y Hunt (2015), ACM TMIS 6(4), doi:10.1145/2843948

(diapositiva 10) Acertar fuera de línea no es lo mismo que retener El Netflix Prize y la lección que Netflix contó después. FUERA DE LÍNEA EN LÍNEA Predecir calificaciones Prueba A/B con clientes El premio de US$1 millón pedía mejorar más de 10% el error (RMSE) de CineMatch con datos históricos. Un grupo ve el algoritmo nuevo y otro el actual. Se compara retención y horas vistas, no el error de predicción.

(diapositiva 10) Gomez-Uribe y Hunt (2015) explican que la medida de precisión fuera de línea no bastaba, y que la decisión final se toma con pruebas A/B. Es lo mismo que vimos con el hit rate contra el ingreso incremental.

(diapositiva 12) Con calificaciones reales: pocos títulos lo concentran todo MovieTweetings: 100,000 calificaciones reales, 16,554 usuarios y 10,506 películas. No son datos de Netflix. 74% 74% de las calificaciones van al 10% de películas más calificadas. de las películas tienen menos de 5 calificaciones: casi no hay datos para recomendarlas. Hit rate@10: ¿aparece en el top 10 la película que le gustó después?

(diapositiva 12) Populares Por ítem (coseno) 14.5% 15.4% 3,859 usuarios con 5 o más películas que les gustaron (7+ de 10); se oculta la última de cada uno. Dooms et al. (2013), MIT.

(diapositiva 13) El experimento: pantalla personalizada contra populares 12,000 suscriptores simulados, la mitad con cada pantalla de inicio. Medida Personalizada Populares Diferencia Retención a 12 meses 76.4% 72.4% +4.0 pts Churn mensual 2.22% 2.66% −0.44 pt CLV por miembro US$136 US$118 +US$18 70% 52% +18 pts Horas vistas por recomendación Intervalo de confianza de 95% para la diferencia de retención: de 2.5 a 5.6 puntos. Hay efecto, y el rango es amplio. Datos simulados con un efecto conocido.

(diapositiva 13) En la vida real el efecto no se conoce: por eso se mide. Fuente: laboratorio de clase (suscriptores_muestra.csv). Simulado, no es de Netflix.

(diapositiva 14) El CAC por canal cambia el orden Al quitar a los clientes que habrían llegado igual, cada canal vale menos de lo que parece.

(diapositiva 14) Canal CLV/CAC contable Habría llegado igual CAC real CLV/CAC real Referidos y orgánico 26.8 50% US$16 13.3 Búsqueda de pago 4.1 40% US$58 2.4 Alianzas (telcos) 3.3 5% US$28 3.1 Redes sociales 2.8 12% US$45 2.5 TV y exteriores 1.9 30% US$100 1.3 La búsqueda de pago cae de 4.1 a 2.4 y pasa del segundo al cuarto lugar, por debajo de las redes sociales (2.5); las alianzas casi no cambian porque casi todos sus clientes son nuevos de verdad.

(diapositiva 18) Un estudio publicado en 2019 en el Journal of Behavioral Decision Making (Yeomans, Shah, Mullainathan y Kleinberg) comparó a un sistema de recomendación con personas recomendando chistes

(diapositiva 19) Cerramos la fórmula: una pregunta por palanca CLV = (ingreso − costo) × r / (1 + d − r), comparado contra el CAC MARGEN RETENCIÓN ARPU CAC ¿Cuánto churn aguanta un aumento? ¿Cuánto churn quita la acción? ¿Acierta o causa? ¿Cuántos habrían llegado igual? Precio +10% se paga hasta 3.3% de churn. Solo un grupo de control lo dice. El hit rate no es ingreso extra. El CAC real es mayor que el contable. Lo común a las cuatro:

(diapositiva 19) la fórmula da el orden de magnitud, y lo que decide es un supuesto que hay que medir (churn, efecto, incrementalidad). Para llevarse: una palanca vale tanto como la confianza que tengamos en el número que la acompaña.
