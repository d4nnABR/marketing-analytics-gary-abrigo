# Anexo — Actividad No. 3 (Grupo 5): Laboratorio de Recomendación

Carrusel «Para ti» · 8,000 clientes · historial de ~10 meses · experimento de 90 días (4,000 tratamiento y 4,000 control).

## Entregables
| Entregable | Dónde |
|---|---|
| Notebook ejecutado (`laboratorio_recomendacion.ipynb`) | [`Semana_4/Tarea/laboratorio_recomendacion.ipynb`](./laboratorio_recomendacion.ipynb) |
| Branch (obligatorio) | https://github.com/d4nnABR/marketing-analytics-gary-abrigo/tree/Tarea_Actividad_3_Grupo_5 |
| App de Streamlit (obligatorio) | Pendiente de desplegar. Archivo principal: `Semana_4/Tarea/app.py` |
| Conclusión de una página | [`CONCLUSION.md`](./CONCLUSION.md) |
| Notebook en Databricks | `/Repos/gdabrigo@correo.url.edu.gt/marketing-analytics-gary-abrigo/Semana_4/Tarea/laboratorio_recomendacion` |

## Tabla de comparación de recomendadores
Hit rate@3 solo en el grupo control (clientes que probaron algo nuevo, 1,797 de 4,000). El ingreso incremental sale de la información oculta que se destapa al final.

| Recomendador | Hit rate@3 (control) | Cobertura (de 28) | Ingreso incremental (US$/cliente) | % de compras acertadas que ya iban a ocurrir |
|---|---:|---:|---:|---:|
| Popularidad | 0.221 | 12 | 0.998 | 30.7% |
| Ítem-based | 0.401 | 28 | 1.191 | 43.8% |
| Cliente-based (K = 30) | 0.306 | 28 | 1.189 | 37.6% |
| Otro modelo: SVD (6 factores) | 0.390 | 28 | 1.173 | 43.5% |
| **Final (ítem + respaldo de popularidad)** | **0.410** | 28 | 1.181 | 44.3% |

Efecto del carrusel (Paso 3): ΔARPU +US$1.11 (IC 95% +0.37 a +1.86) · Δmargen neto +US$0.51 (IC 95% +0.05 a +0.98) · ΔCLV ≈ US$1.60 por cliente. El efecto verdadero (US$0.99) cae dentro del intervalo.

## Decisiones de método
- **Modelo libre (TODO 4):** SVD truncado. Se probaron 2, 4, 6, 8, 12, 16 y 24 factores y se escogió 6 (hit rate 0.390). La elección usó el mismo grupo de control con el que se evalúa, así que ese resultado es ligeramente optimista.
- **Empates:** en esta base hay muchos puntajes idénticos (por ejemplo, entre clientes con las mismas compras), y `np.argsort` los ordena de forma distinta según el entorno. Para que el notebook y la app den **los mismos números en cualquier máquina** (local o Databricks), `top_k` usa `kind="stable"` y las similitudes se redondean a 6 decimales antes de ordenar. Es la única modificación a las piezas que venían armadas.
- **Clientes sin historial (334):** los métodos colaborativos les dan puntaje 0 a todo; el recomendador final les muestra la popularidad.

## Cómo reproducir
```bash
cd Semana_4/Tarea
pip install -r requirements.txt            # app: streamlit, pandas, numpy, scikit-learn
streamlit run app.py
```
El notebook además usa `matplotlib` y `jupyter`. Los datos están en `Semana_4/Tarea/data/`; la revelación usa `verdad_oculta_cliente_producto.csv` y `verdad_oculta_clientes.csv`, que están en la misma carpeta.

En Databricks los mismos CSV están en el Volume `/Volumes/workspace/default/semana4/`; el notebook lee la copia de `data/` del Git folder.

## App de Streamlit
- **Recomendar:** se elige un cliente y un método; muestra las 3 recomendaciones con puntaje, precio y el «porque» (por ítem, los productos comprados más parecidos; por cliente, cuántos de sus K vecinos lo compraron; popularidad, qué parte de la base lo compra).
- **Comparar métodos:** hit rate@3, precisión@3 y cobertura sobre el grupo control, con un slider de cuántos clientes evaluar.
- **La verdad oculta:** casilla opcional que compara el hit rate con el ingreso incremental.
- **Controles interactivos:** selector de método, slider de vecinos (K), slider de factores del SVD y slider de clientes a evaluar.

## Datos
Simulados. Los efectos fueron plantados por el generador del laboratorio; sirven para practicar el método y no prueban que una cadena real obtenga estos resultados.
