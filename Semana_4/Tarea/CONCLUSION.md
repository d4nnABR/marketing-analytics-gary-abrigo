# Carrusel «Para ti»: recomendación al Presidente de Marketing

**Recomendación.** Extender el carrusel a toda la base con el recomendador **filtrado por ítem + popularidad como respaldo**, por fases y con un grupo de control permanente.

## Resultado del experimento
Carrusel de popularidad, 90 días, 4,000 clientes tratados y 4,000 de control al azar.

| Medida | Resultado |
|---|---|
| ΔARPU por cliente | +US$1.11 (IC 95%: +0.37 a +1.86) |
| Δmargen neto (costo US$0.20) | +US$0.51 (IC 95%: +0.05 a +0.98) |
| ΔCLV por cliente (r = 0.78, d = 0.03) | ≈ US$1.60 (≈ US$6,400 en los 4,000 tratados) |

El carrusel se paga, pero con poco margen: el límite inferior del margen neto apenas pasa de cero. El ΔCLV supone que el efecto dura mientras el cliente siga activo.

## Comparación de recomendadores
| Recomendador | Hit rate@3 (control) | Ingreso incremental (US$/cliente) |
|---|---|---|
| Popularidad | 0.221 | 0.998 |
| Filtrado por ítem | 0.401 | 1.191 |
| Filtrado por cliente | 0.306 | 1.189 |
| SVD (6 factores) | 0.390 | 1.173 |
| **Final (ítem + respaldo)** | **0.410** | **1.181** |

El recomendador final acierta casi el doble que la popularidad y recomienda los 28 productos (la popularidad, 12). Es explicable («porque compró X») y cubre a los clientes sin historial.

## Hit rate e ingreso extra
Un hit rate alto no implica ingreso extra en la misma proporción. El filtrado por ítem supera a la popularidad en 81% de hit rate, pero solo en 19% de ingreso incremental. Entre 31% y 44% de las compras acertadas ya iban a ocurrir sin recomendación. El efecto medido (US$1.11) quedó cerca del verdadero (US$0.99).

## Siguientes pasos
1. Prueba A/B de tres brazos (control, popularidad y recomendador final) durante 90 días, con ARPU y margen neto por cliente.
2. Mostrar el carrusel según la receptividad: el ingreso incremental va de US$0.47 (cuartil menos receptivo) a US$1.98 (más receptivo).

Los datos son simulados. El número de factores del SVD se eligió con el grupo de control, por lo que su hit rate es algo optimista.
