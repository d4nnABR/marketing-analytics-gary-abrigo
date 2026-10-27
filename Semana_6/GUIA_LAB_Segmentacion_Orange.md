# Lab de Orange · Segmentación de clientes (≈60 min)

**Pregunta de negocio:** ¿a qué grupos de clientes les hablamos distinto, y cuánto vale cada grupo?

## Archivos
| Archivo | Qué es |
|---|---|
| `clientes_retail.csv` | **Real.** 2,205 clientes de un retailer de alimentos (versión limpia de "Customer Personality Analysis", base abierta). Ingreso, edad, hijos, gasto por categoría, compras por canal, recencia y respuesta a campañas |
| `formas_lunas.csv` | **Sintético.** 400 puntos en forma de dos lunas + 20 de ruido. Sirve para ver dónde falla k-means |
| `formas_alargadas.csv` | **Sintético.** 3 grupos alargados e inclinados. Sirve para el notebook (mezclas gaussianas) |

Nota: `gasto_total` ya es la suma de vinos, frutas, carnes, pescado y dulces. `gasto_premium` es una parte de ese total, no se suma.

## Parte 1 · Conozca los datos (10 min)
1. **File** → `clientes_retail.csv`. Conecte **Data Table** y **Distributions** (`gasto_total`).
2. ¿Cómo se ve `gasto_total`? (Pocos clientes gastan mucho, muchos gastan poco.)

## Parte 2 · k-means: el punto de partida (15 min)
1. **Select Columns**: deje como atributos solo `ingreso_anual`, `gasto_total`, `compras_tienda`, `compras_web`, `compras_catalogo`, `visitas_web_mes`, `recencia_dias`, `hijos_pequenos`, `edad`. Todo lo demás a "Ignored" o "Meta".
2. **Continuize / Normalize** (estandarizar por desviación): si no se normaliza, el ingreso (decenas de miles) aplasta a las visitas web (unidades).
3. **k-Means** con "From 2 to 8" y mire la silueta de cada k.
4. Fije **k = 3** y conecte a **Scatter Plot** (x = `ingreso_anual`, y = `gasto_total`, color = Cluster).
5. **Group By** (o **Box Plot** por Cluster): promedio de cada variable por segmento.

**Preguntas:** ¿qué k tiene mejor silueta? ¿Es muy alta? ¿Ponga un nombre de negocio a cada segmento?

## Parte 3 · Compare técnicas (15 min)
1. Con los datos normalizados, conecte **Distances** (Euclidean) → **Hierarchical Clustering** (Ward). Corte en 3 grupos.
2. Conecte los datos normalizados a **DBSCAN**. Use el gráfico de distancia al k-ésimo vecino para escoger `eps`; pruebe cerca de 1.5 y compare con 2 o 3.
3. Compare cuántos clientes caen en cada grupo con cada técnica (**Merge Data** o **Scatter Plot** coloreado).

**Preguntas:** ¿las tres técnicas dan los mismos grupos? ¿Qué pasa con DBSCAN al subir `eps`? ¿Cuál le serviría más a marketing para actuar?

## Parte 4 · ¿Cuánto vale cada segmento? (10 min)
1. Con los grupos de k-means (k = 3), calcule por segmento: número de clientes, gasto promedio y % del gasto total (**Group By** + **Formula**).
2. Mire también `respondio_ultima_campana` por segmento.

**Preguntas:** ¿qué % de clientes genera qué % del gasto? ¿A qué segmento le gastaría el presupuesto de la próxima campaña y por qué? (Recuerde el CLV/CAC de las semanas anteriores.)

**Guarde su segmentación (la usará en la tarea):**
1. Conecte la salida *Data* de **k-Means** (k = 3) a **Save Data**.
2. Formato **CSV**, nombre `clientes_con_cluster.csv`.
3. Ábralo y compruebe que trae la columna `Cluster` con los valores C1, C2 y C3.

Nota: lo más simple en Orange es guardar la asignación de cada cliente. Un archivo `.joblib` no es el formato de Orange; los modelos de Python (notebook) sí se guardan así.

## Parte 5 · Datos sintéticos: cuando k-means falla (10 min)
1. **File** → `formas_lunas.csv`. **Scatter Plot** (x, y; color = `grupo_real`).
2. **k-Means** con k = 2 y mire cómo parte las lunas. Luego **DBSCAN** directo sobre `x` e `y` (sin estandarizar): pruebe eps ≈ 0.2 y min vecinos = 5. Pruebe también eps = 0.1.
3. Compare con `grupo_real`.

**Preguntas:** ¿por qué k-means corta mal? ¿Qué hizo DBSCAN con el ruido? ¿Cuándo sospecharía que sus clientes no tienen forma de "bolas"?

## Cierre
Escriba en 3 líneas: qué segmentación recomendaría a marketing, con qué técnica y por qué.

*Lo que Orange no trae (mezclas gaussianas y k-prototypes) está en el notebook, que es parte de la **tarea** (ver `TAREA_Segmentacion.md`).*
