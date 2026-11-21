# Venta cruzada y sistemas de recomendación

## Reglas de asociación (Apriori)
Regla A → B ("quien compra A también compra B"):
- Soporte(A) = canastas con A ÷ total de canastas.
- Soporte(A y B) = canastas con A y B ÷ total.
- Confianza(A → B) = soporte(A y B) ÷ soporte(A) = probabilidad de B dado A.
- Lift(A → B) = confianza(A → B) ÷ soporte(B). Lift > 1: se compran juntos más de lo esperado por azar. Lift = 1: independientes. Lift < 1: se evitan.

Ejemplo resuelto: 1,000 canastas; A en 200, B en 150, A y B juntos en 60.
Soporte(A) = 0.20; soporte(B) = 0.15; soporte(A y B) = 0.06.
Confianza = 0.06 ÷ 0.20 = 0.30 (30%). Lift = 0.30 ÷ 0.15 = 2.0.

Apriori filtra primero los conjuntos con soporte mínimo (si un producto es poco frecuente, cualquier combinación con él también lo es).

## Filtrado colaborativo
- Por ítem (item-based): recomienda productos parecidos a los que el cliente ya compró; la similitud se calcula entre columnas de la matriz cliente × producto (por ejemplo, similitud del coseno).
- Por cliente (user-based): busca clientes parecidos y recomienda lo que ellos compraron.

## Medición
Se separa un periodo de prueba (holdout). Hit rate@k = proporción de clientes para los que al menos uno de los k productos recomendados fue comprado en el holdout. Lo que importa al negocio es el ingreso incremental frente a un grupo sin recomendaciones, no solo el hit rate. La venta cruzada sube el ARPU (ingreso promedio por usuario) y por tanto el CLV.
