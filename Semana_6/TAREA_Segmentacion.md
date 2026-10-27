# Tarea · Segmentación de clientes (notebook + app en Streamlit)

**Pregunta de negocio:** ¿qué segmentación le recomendaría a marketing, y puede un compañero verla y compararla sin abrir su código?

## Qué entregar
1. **Notebook ejecutado** (`notebook_segmentacion.ipynb`) con las preguntas respondidas: mezclas gaussianas y k-prototypes. Al final guarda `segmentos_notebook.csv`, `modelo_gmm.joblib` y `modelo_kproto.joblib`.
2. **App en Streamlit** (`app.py` y `requirements.txt`) con dos partes:
   - **Visor de grupos:** sube un CSV con una columna de grupos (el que guardó desde Orange o el del notebook) y muestra los clientes por grupo en un gráfico y una tabla de perfil (clientes, % de clientes, gasto promedio, % del gasto).
   - **Comparador de técnicas:** ajusta k-means, jerárquico, DBSCAN, mezcla gaussiana y k-prototypes con las mismas variables y muestra, para cada una, cuántos grupos salen, sus tamaños, la silueta y qué tanto coincide con las demás.
3. **Recomendación en 3 líneas:** qué segmentación le daría a marketing, con qué técnica y por qué.

## Cómo avanzar
- Orange: guarde su k-means con **Save Data** (CSV con columna `Cluster`).
- Notebook: ejecútelo en Google Colab o Jupyter con los dos CSV en la misma carpeta.
- App: `pip install streamlit pandas scikit-learn plotly kmodes` y luego `streamlit run app.py`.
- Piezas útiles: `st.file_uploader`, `st.tabs`, `st.selectbox`, `st.slider`, `st.dataframe`, `plotly.express.scatter`.
- Puede apoyarse en un asistente de IA para escribir el código, pero debe poder explicar qué hace cada parte.

## Preguntas para el comentario final
- ¿Las cinco técnicas coinciden? ¿Cuáles se parecen más y por qué?
- ¿Agregar educación y estado civil (k-prototypes) cambió los grupos?
- ¿Qué técnica sería más fácil de explicarle a marketing?
