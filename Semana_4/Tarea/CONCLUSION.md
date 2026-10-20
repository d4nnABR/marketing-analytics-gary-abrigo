# Carrusel «Para ti»: recomendación para el Presidente de Marketing

**Recomendación.** Sí, extender el carrusel al resto de la base, usando el recomendador **«filtrado por ítem con popularidad como respaldo»**, y hacerlo por fases con un grupo de control permanente para seguir midiendo el efecto.

## Qué mostró el experimento
El carrusel (3 productos populares) se probó 90 días con 4,000 clientes tratados y 4,000 de control, elegidos al azar. La diferencia entre grupos es el efecto causal:

| Medida | Resultado |
|---|---|
| ΔARPU por cliente | **+US$1.11** (IC 95%: +0.37 a +1.86) |
| Δmargen neto, después del costo de US$0.20 | **+US$0.51** (IC 95%: +0.05 a +0.98) |
| ΔCLV por cliente (r = 0.78, d = 0.03, por trimestre) | **≈ US$1.60**, unos US$6,400 para los 4,000 tratados |

El carrusel se paga, pero con poco margen de seguridad: el extremo inferior del margen neto apenas supera el cero y el ΔCLV supone que el efecto se mantiene mientras el cliente siga activo, lo que no está probado.

## Qué recomendador llevar y por qué
| Recomendador | Hit rate@3 (control) | Ingreso incremental (US$/cliente) |
|---|---|---|
| Popularidad (el del experimento) | 0.221 | 0.998 |
| Filtrado por ítem | 0.401 | 1.191 |
| Filtrado por cliente | 0.306 | 1.189 |
| SVD (6 factores) | 0.390 | 1.173 |
| **Final (ítem + respaldo)** | **0.410** | **1.181** |

El recomendador final acierta casi el doble que la popularidad, recomienda los 28 productos del catálogo (la popularidad solo 12), es barato de calcular, explicable («porque compraste X») y cubre a los clientes sin historial con el respaldo de popularidad, donde el filtrado por ítem solo acierta 16% y el respaldo 34%.

## Qué tan cerca estuvo el hit rate de la verdad
Poco. El hit rate dice que el filtrado por ítem es **81% mejor** que la popularidad, pero su ingreso incremental es solo **19% mayor** (US$1.19 contra US$1.00 por cliente). Entre el 31% y el 44% de las compras que los métodos aciertan ya iban a ocurrir sin recomendación. Un reporte que solo mire el hit rate exagera la mejora de ARPU. Además, el efecto medido en el experimento (US$1.11) estuvo cerca del efecto verdadero (US$0.99) y dentro del intervalo, pero el intervalo es ancho.

## Cómo seguir
1. Lanzar el recomendador final en una prueba A/B de tres brazos (control, popularidad y final) durante 90 días, midiendo ARPU y margen neto por cliente, y vigilando el efecto de novedad semana a semana.
2. No mostrar el carrusel a todos por igual: el ingreso incremental esperado sube de US$0.47 en el cuartil menos receptivo a US$1.98 en el más receptivo. Un modelo de uplift (como el de la Semana 3) permitiría concentrar el carrusel donde más rinde y evitar la sensación de «creepy» en quienes no responden.

**Nota sobre los datos.** Los datos son simulados y los efectos fueron plantados por el generador; sirven para practicar el método y no prueban que una cadena real obtenga estos resultados. El número de factores del SVD se eligió con el mismo grupo de control con que se evalúa, así que el hit rate de ese modelo es ligeramente optimista.
