# Entregables — Actividad 2 (Grupo 5)

Campaña **Starbucks Rewards** · cupón de $5 · ventana de 60 días · Churn + Uplift Modeling.

| Entregable | Enlace |
|---|---|
| **Notebook ejecutado** (`laboratorio_final.ipynb`) | https://github.com/d4nnABR/marketing-analytics-gary-abrigo/blob/Tarea_Actividad_2_Grupo_5/Semana_3/laboratorio_final.ipynb |
| **Branch** `Tarea_Actividad_2_Grupo_5` (obligatorio) | https://github.com/d4nnABR/marketing-analytics-gary-abrigo/tree/Tarea_Actividad_2_Grupo_5 |
| **App de Streamlit** (obligatorio) | https://marketing-analytics-gary-abrigo-42phkecnur6sgubz3hxmae.streamlit.app/ |
| Conclusión de una página | [`Semana_3/CONCLUSION.md`](./CONCLUSION.md) |

## Detalle por punto de la rúbrica

1. **Notebook** `laboratorio_final.ipynb` — ejecutado de punta a punta, con las preguntas de cada
   paso respondidas y los outputs/gráficas incluidos.
2. **Branch** `Tarea_Actividad_2_Grupo_5` — creada a partir de `main` con estos entregables.
3. **App de Streamlit** (`Semana_3/app.py`) — construida sobre `streamlit_starter.py`. Muestra la
   **curva Qini del T-learner** y la **tabla de políticas del Paso 3**, con un **slider
   interactivo** para elegir el % de la base a contactar y un **selector Español/English**.
4. **Tabla de comparación de modelos** (Qini y correlación con el uplift real):

   | Modelo dentro del T-learner | Correlación con el uplift real | Qini |
   |---|---:|---:|
   | Random Forest (regularizado) | 0.868 | +0.158 |
   | Gradient Boosting | 0.838 | +0.156 |
   | SVM (RBF) | 0.797 | +0.146 |
   | Árbol de decisión (`max_depth=5`) | 0.776 | +0.142 |
   | Regresión logística (base del notebook) | 0.619 | +0.142 |

   > Nota: los valores “ejemplo” de la rúbrica no son los nuestros; estos son los resultados
   > reales obtenidos al ejecutar el notebook.

5. **Conclusión de una página** — recomendación de contactar al **20 % de mayor uplift**
   (valor neto total máximo, +$2,368.51 en prueba), respaldada por la comparación de modelos.

## Cómo reproducir

```bash
cd Semana_3
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace laboratorio_final.ipynb
streamlit run app.py
```
