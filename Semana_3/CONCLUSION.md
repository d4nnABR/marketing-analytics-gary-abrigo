# Conclusión ejecutiva — Campaña Starbucks Rewards (cupón de $5, ventana de 60 días)

**Para:** Presidencia de Marketing
**De:** Equipo de Analítica de Marketing — Grupo 5
**Asunto:** A qué porcentaje de la base contactar y qué tan confiable es el modelo

---

## Recomendación

**Contactar al 20 % de la base con mayor uplift estimado** (los 2,400 clientes mejor
priorizados dentro del conjunto de prueba). Es el punto donde el **valor neto total es máximo**:
**+$2,368.51**, frente a +$1,948.93 al contactar solo al 10 %. Pasado ese punto el valor cae y se
vuelve negativo: contactar al 40 % o más **destruye valor** (−$500.97 al 40 %; −$20,236.13 al
100 %).

En otras palabras: el cupón no se debe repartir por volumen ni por “compra reciente”, sino
**concentrarse en el segmento persuadible** — quien no compraría si no recibe el cupón, pero sí
compra cuando lo recibe.

## Evidencia que respalda la decisión

| % de la base contactada | Valor por cliente | Valor neto total |
|---:|---:|---:|
| 10 % | **+$1.62** (máximo por cliente) | +$1,948.93 |
| **20 %** | +$0.99 | **+$2,368.51 (máximo)** |
| 30 % | +$0.46 | +$1,673.33 |
| 40 % en adelante | negativo | negativo |

- El **modelo de uplift (T-learner)** ordena a los clientes casi **3× mejor** que un modelo de
  riesgo/churn tradicional (Qini **+0.142** vs. +0.048). Targetear por riesgo apenas supera el
  azar (+$0.07 por cliente) porque el churn identifica a quien se va, no a quien el cupón
  convence.
- Solo el **22.4 % de la base es realmente “persuadible”**; el resto son *Sure Things* (compran
  igual, 48.9 %), *Lost Causes* (no compran ni con cupón, 21.5 %) y *Sleeping Dogs* (compran
  menos si se les molesta, 7.2 %). Regalar cupones fuera del segmento persuadible es margen
  perdido.
- Un **modelo de clasificación mejorado (Random Forest)** alcanza una correlación de **0.868**
  con el uplift real y un Qini de **+0.158**, superando a la regresión logística base (0.619 y
  +0.142). Gradient Boosting (0.838) y SVM (0.797) quedan muy cerca.

## Confiabilidad del modelo

El uplift estimado por el mejor modelo (Random Forest) **correlaciona 0.868 con el uplift
verdadero**, es decir, reproduce ~87 % de la señal real de persuabilidad. Esto da alta confianza
para usar el ranking como criterio de asignación del cupón. La logística base, aunque más simple,
ya capturaba la señal principal (0.619), pero migrar a Random Forest **casi cuadruplica** la
precisión del ordenamiento.

## Riesgos y siguientes pasos

1. **Sobreajuste:** los árboles sin límite estiman uplift con ruido; la comparación se hizo con
   `max_depth` / `min_samples_leaf` para que la mejora sea real. Recomendamos promover el Random
   Forest regularizado, no un árbol libre.
2. **Estimar antes de gastar:** validar el 20 % con una campaña piloto y medir el valor neto real
   antes de escalar a toda la base.
3. **Revisar márgenes:** el resultado depende del costo del cupón ($5) y del margen por cliente;
   cualquier cambio de precio exige recalcular el punto óptimo.

**Decisión propuesta:** aprobar el contacto al **20 % de mayor uplift** (≈2,400 clientes por cada
12,000 en prueba) usando el modelo Random Forest, con un piloto de control para confirmar el
retorno antes del despliegue completo.
