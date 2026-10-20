# Anexo — Actividad 3 (Grupo 5): Laboratorio de Recomendación

## Entregables
| Entregable | Dónde |
|---|---|
| Notebook ejecutado | [`laboratorio_recomendacion.ipynb`](./laboratorio_recomendacion.ipynb) |
| Branch | https://github.com/d4nnABR/marketing-analytics-gary-abrigo/tree/Tarea_Actividad_3_Grupo_5 |
| App de Streamlit | Pendiente de desplegar. Archivo: [`app.py`](./app.py) |
| Conclusión | [`CONCLUSION.md`](./CONCLUSION.md) |
| Databricks | `/Repos/gdabrigo@correo.url.edu.gt/marketing-analytics-gary-abrigo/Semana_4/Tarea/laboratorio_recomendacion` |

## Comparación de recomendadores
Hit rate@3 en el grupo control (1,797 de 4,000 clientes probaron algo nuevo).

| Recomendador | Hit rate@3 | Cobertura (de 28) | Ingreso incremental (US$/cliente) | % de aciertos que ya iban a ocurrir |
|---|---:|---:|---:|---:|
| Popularidad | 0.221 | 12 | 0.998 | 30.7% |
| Ítem-based | 0.401 | 28 | 1.191 | 43.8% |
| Cliente-based (K = 30) | 0.306 | 28 | 1.189 | 37.6% |
| SVD (6 factores) | 0.390 | 28 | 1.173 | 43.5% |
| **Final (ítem + respaldo)** | **0.410** | 28 | 1.181 | 44.3% |

Efecto del carrusel: ΔARPU +US$1.11 (IC 95%: +0.37 a +1.86), Δmargen neto +US$0.51, ΔCLV ≈ US$1.60 por cliente. El efecto verdadero (US$0.99) cae dentro del intervalo.

## Decisiones
- **SVD:** 6 factores, el de mayor hit rate entre 2, 4, 6, 8, 12, 16 y 24. Se eligió con el grupo de control, por lo que es algo optimista.
- **Empates:** `top_k` ordena con `kind="stable"` y las similitudes se redondean a 6 decimales, para obtener los mismos resultados en cualquier equipo.
- **Clientes sin historial (334):** el recomendador final les muestra la popularidad.

## App de Streamlit
Bilingüe (ES/EN), con el tema de las demás apps.
- **Recomendaciones:** 3 productos por cliente con puntaje, precio y «porque».
- **Comparación de métodos:** hit rate@3, precisión@3 y cobertura en el grupo control.
- **Verdad oculta:** hit rate frente a ingreso incremental.
- **Controles:** idioma, método, ID de cliente, vecinos (K) y factores del SVD.

```bash
cd Semana_4/Tarea
pip install -r requirements.txt
streamlit run app.py
```

Datos simulados.
