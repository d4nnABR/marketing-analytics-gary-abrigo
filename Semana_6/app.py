# Archivo base para el despliegue del Agente en Streamlit

import pandas as pd
import joblib

# 1. Cargar el dataset con los segmentos asignados
df_clientes = pd.read_csv("segmentos_notebook.csv")
print("Dataset de clientes cargado con éxito. Filas:", len(df_clientes))
display(df_clientes.head())

# 2. Cargar los modelos entrenados (.joblib)
gmm_bundle = joblib.load("modelo_gmm.joblib")
kproto_bundle = joblib.load("modelo_kproto.joblib")

print("\nModelos cargados correctamente desde los archivos .joblib")

# Extraer componentes del GMM
scaler = gmm_bundle["scaler"]
modelo_gmm = gmm_bundle["modelo"]
vars_num_gmm = gmm_bundle["variables"]
print("Variables numéricas GMM:", vars_num_gmm)

# Extraer componentes de K-Prototypes
modelo_kproto = kproto_bundle["modelo"]
vars_num_kp = kproto_bundle["variables_numericas"]
vars_cat_kp = kproto_bundle["variables_categoricas"]
print("Variables numéricas K-Proto:", vars_num_kp)
print("Variables categóricas K-Proto:", vars_cat_kp)