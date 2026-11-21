"""agente.py · El agente de Marketing Analytics en un archivo de Python.

Es el mismo agente del notebook (el taller), listo para que la app de Streamlit (app.py) lo use.
Cómo completarlo: reemplacen cada función que tiene espacios COMPLETAR por su versión terminada del notebook.
Para revisar que quedó bien, corran el Paso 10.2 del notebook.
"""

# ============================================================ 1. Conexión con Gemini

import os, re, json, time, glob, difflib, unicodedata
import numpy as np
import pandas as pd
from google import genai
from google.genai import types, errors

try:
    from google.colab import userdata          # Colab: llave en Secrets
    API_KEY = userdata.get("GEMINI_API_KEY")
except ImportError:                            # VS Code: llave en el archivo .env
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Elegir un modelo "flash-lite" disponible en su cuenta
excluir = ("tts", "image", "live", "audio", "embedding", "preview", "exp")
modelos = []
for m in client.models.list():
    nombre = m.name.replace("models/", "")
    if "generateContent" in (m.supported_actions or []) and "gemini" in nombre:
        if not any(x in nombre for x in excluir):
            modelos.append(nombre)
lite = sorted(m for m in modelos if "flash-lite" in m)
MODELO = lite[-1] if lite else sorted(modelos)[-1]
print("Modelo:", MODELO)

D_MENSUAL = 0.008    # tasa de descuento mensual del curso (0.8%)

# ============================================================ 2. Fuentes de datos (cámbienlas para usar sus datos)

# Cada fuente dice: dónde está el archivo y cómo se llaman SUS columnas.
# "columnas" = {nombre_estándar_que_usa_la_herramienta: nombre_de_la_columna_en_SU_archivo}
# Para usar sus propios datos, solo cambien "ruta" y el lado derecho de "columnas".
# "ruta" puede ser un archivo local (.csv, .xlsx, .parquet, .json) o una dirección web (URL).
FUENTES = {
    "precios": {
        "descripcion": "Pruebas de precio: a cada precio, cuántas unidades se vendieron al mes (caso Nube Fit)",
        "ruta": "datos/pruebas_precio.csv",
        "columnas": {"segmento": "segmento", "precio": "precio", "unidades": "unidades"},
    },
    "tickets": {
        "descripcion": "Tickets de compra: un renglón por producto comprado (Semana 4, cafetería)",
        "ruta": "datos/tickets.csv",
        "columnas": {"ticket": "order_id", "producto": "item"},
    },
    "clientes": {
        "descripcion": "Clientes de una tienda con ingreso, gasto, compras por canal y edad (Semana 6)",
        "ruta": "datos/clientes_retail.csv",
        "columnas": {"id": "id_cliente", "gasto": "gasto_total"},
        # Columnas numéricas con las que se agrupan los clientes (nombres de SU archivo)
        "variables": ["ingreso_anual", "gasto_total", "compras_tienda", "compras_web", "compras_catalogo",
                      "visitas_web_mes", "recencia_dias", "hijos_pequenos", "edad"],
    },
}

CARPETA_APUNTES = "apuntes"    # carpeta con los apuntes del curso (.md o .txt) para buscar_apunte

# Las rutas relativas se buscan junto a este archivo (así la app funciona desde cualquier carpeta)
_BASE = os.path.dirname(os.path.abspath(__file__))
for _conf in FUENTES.values():
    if not _conf["ruta"].startswith(("http://", "https://", "/")) and not os.path.isabs(_conf["ruta"]):
        _conf["ruta"] = os.path.join(_BASE, _conf["ruta"])
if not os.path.isabs(CARPETA_APUNTES):
    CARPETA_APUNTES = os.path.join(_BASE, CARPETA_APUNTES)

_CACHE = {}     # para no leer el mismo archivo cada vez


def cargar_datos(nombre):
    """Lee la fuente `nombre` de FUENTES y devuelve una tabla con los nombres de columna estándar.
    Si algo falla, lanza un ValueError con un mensaje claro."""
    if nombre not in FUENTES:
        raise ValueError(f"No existe la fuente '{nombre}'. Fuentes disponibles: {list(FUENTES)}")
    if nombre in _CACHE:
        return _CACHE[nombre].copy()

    conf = FUENTES[nombre]
    ruta = conf["ruta"]
    extension = ruta.lower().split("?")[0].rsplit(".", 1)[-1]
    try:
        if extension in ("xlsx", "xls"):
            df = pd.read_excel(ruta)
        elif extension == "parquet":
            df = pd.read_parquet(ruta)
        elif extension == "json":
            df = pd.read_json(ruta)
        else:
            df = pd.read_csv(ruta)
    except Exception as e:
        raise ValueError(f"No pude leer '{ruta}' para la fuente '{nombre}': {e}")

    # Limpia los nombres de columna (quita espacios y prefijos de Orange como "m#")
    df.columns = [str(c).split("#")[-1].strip() for c in df.columns]

    # Revisa que estén las columnas que dice FUENTES
    faltan = [su_col for su_col in conf["columnas"].values() if su_col not in df.columns]
    faltan += [v for v in conf.get("variables", []) if v not in df.columns]
    if faltan:
        raise ValueError(f"La fuente '{nombre}' no tiene las columnas {faltan}. "
                         f"Columnas del archivo: {list(df.columns)}")

    # Renombra: nombre de SU archivo → nombre estándar (sin borrar las demás columnas)
    for estandar, su_col in conf["columnas"].items():
        df[estandar] = df[su_col]

    _CACHE[nombre] = df
    return df.copy()


def listar_fuentes() -> dict:
    """Lista las fuentes de datos disponibles: para qué sirve cada una, sus columnas y
    ejemplos de valores (por ejemplo, los nombres de los segmentos o de los productos).
    Úsala cuando no sepas qué segmento, producto o fuente existe."""
    resumen = {}
    for nombre, conf in FUENTES.items():
        try:
            df = cargar_datos(nombre)
            ejemplos = {}
            for estandar in conf["columnas"]:
                if not pd.api.types.is_numeric_dtype(df[estandar]):
                    ejemplos[estandar] = [str(x) for x in df[estandar].value_counts().index[:30]]
            resumen[nombre] = {"descripcion": conf["descripcion"], "filas": len(df),
                               "columnas": list(conf["columnas"]), "ejemplos": ejemplos}
        except ValueError as e:
            resumen[nombre] = {"descripcion": conf["descripcion"], "error": str(e)}
    return resumen

# ============================================================ 3. Herramientas del laboratorio

def calcular_clv(margen_mensual: float, churn_mensual: float) -> dict:
    """Calcula el CLV (Customer Lifetime Value, valor de vida del cliente) con la fórmula
    del curso: CLV = m × (1 − c) ÷ (c + d), con d = 0.008 (0.8% mensual).
    margen_mensual: margen por cliente al mes en US$.
    churn_mensual: proporción de clientes que se va cada mes (0.04 = 4%)."""
    if churn_mensual <= 0 or churn_mensual >= 1:
        return {"error": "El churn debe estar entre 0 y 1 (0% y 100%). Si dijeron 4, pregunta si es 4% (0.04)."}
    if margen_mensual <= 0:
        return {"error": "El margen debe ser mayor que 0."}
    m, c, d = margen_mensual, churn_mensual, D_MENSUAL
    return {"clv": round(m * (1 - c) / (c + d), 2)}


def churn_maximo_tolerable(margen_nuevo: float, clv_actual: float) -> dict:
    """Churn mensual máximo que puede tener un segmento después de un cambio de precio
    sin que su CLV baje: c' = (m' − CLV × d) ÷ (m' + CLV), con d = 0.008.
    margen_nuevo: margen mensual por cliente con el precio nuevo (US$).
    clv_actual: CLV de hoy del segmento (US$)."""
    if margen_nuevo <= 0 or clv_actual <= 0:
        return {"error": "El margen nuevo y el CLV actual deben ser mayores que 0."}
    c = (margen_nuevo - clv_actual * D_MENSUAL) / (margen_nuevo + clv_actual)
    if c < 0:
        return {"error": "Con ese margen nuevo ningún churn mantiene el CLV: el margen es menor que CLV × 0.008."}
    return {"churn_maximo": round(c, 4)}


def valor_campana_retencion(clientes_contactados: int, uplift: float,
                            clv: float, costo_por_contacto: float) -> dict:
    """Valor esperado de una campaña de retención usando uplift (efecto incremental:
    proporción de contactados que se queda GRACIAS a la campaña, medido contra un grupo de control).
    clientes_contactados: número de clientes a contactar.
    uplift: proporción retenida por la campaña (0.05 = 5%).
    clv: valor de vida de un cliente retenido (US$).
    costo_por_contacto: costo de contactar a un cliente (US$)."""
    if uplift < 0 or uplift > 1:
        return {"error": "El uplift debe estar entre 0 y 1. Si dijeron 5, pregunta si es 5% (0.05)."}
    if clientes_contactados <= 0 or clv <= 0 or costo_por_contacto < 0:
        return {"error": "Clientes y CLV deben ser mayores que 0, y el costo no puede ser negativo."}
    retenidos = clientes_contactados * uplift
    valor = retenidos * clv
    costo_total = clientes_contactados * costo_por_contacto
    beneficio = valor - costo_total
    return {"clientes_retenidos_extra": round(retenidos, 1), "valor_generado": round(valor, 2),
            "costo_total": round(costo_total, 2), "beneficio_neto": round(beneficio, 2),
            "conviene": beneficio > 0, "uplift_minimo_para_no_perder": round(costo_por_contacto / clv, 4)}

# ============================================================ 4. Herramientas nuevas (REEMPLACEN las que tienen COMPLETAR por las suyas)

def relacion_clv_cac(clv: float, cac: float, margen_mensual: float) -> dict:
    """Compara el CLV (valor de vida del cliente) con el CAC (Customer Acquisition Cost,
    costo de adquirir un cliente) y calcula en cuántos meses se recupera el CAC.
    clv: valor de vida del cliente (US$). cac: costo de adquirir un cliente (US$).
    margen_mensual: margen por cliente al mes (US$).
    Regla del curso: CLV/CAC de 3 o más es sano."""
    # Baranda: los tres datos tienen que ser positivos
    if COMPLETAR:                                     # pista: clv <= 0 or cac <= 0 or margen_mensual <= 0
        return {"error": "CLV, CAC y margen mensual deben ser mayores que 0."}
    razon = COMPLETAR                                 # pista: clv ÷ cac
    meses = COMPLETAR                                 # pista: cac ÷ margen_mensual
    if razon >= 3:
        lectura = "sano (3 o más)"
    elif razon >= 1:
        lectura = "rentable pero ajustado (entre 1 y 3)"
    else:
        lectura = "pierde dinero (menos de 1): cuesta más traer al cliente de lo que deja"
    return {"clv_sobre_cac": round(razon, 2), "meses_para_recuperar_cac": round(meses, 1), "lectura": lectura}

def estimar_elasticidad(segmento: str = "", fuente: str = "precios") -> dict:
    """Estima la elasticidad precio ε con una regresión de ln(unidades) contra ln(precio),
    usando las pruebas de precio de la fuente de datos. ε = cuántos % cambian las ventas
    por cada 1% que sube el precio (negativa: si sube el precio, se vende menos).
    segmento: nombre del segmento (vacío = todos los datos). fuente: nombre de la fuente (por defecto "precios")."""
    # 1. Leer los datos (si la fuente falla, devolvemos el error en vez de caernos)
    try:
        df = cargar_datos(fuente)
    except ValueError as e:
        return {"error": str(e)}

    # 2. Quedarnos con el segmento pedido
    if segmento:
        if "segmento" not in df.columns:
            return {"error": f"La fuente '{fuente}' no tiene columna de segmento."}
        disponibles = sorted(df["segmento"].astype(str).unique())
        df = df[df["segmento"].astype(str).str.lower() == segmento.lower()]
        if COMPLETAR:                                 # pista: df.empty  (no quedó ningún renglón)
            return {"error": f"No existe el segmento '{segmento}'. Segmentos disponibles: {disponibles}"}

    # 3. Baranda: precios y unidades positivos, y al menos 3 precios distintos
    df = df[(df["precio"] > 0) & (df["unidades"] > 0)]
    if df["precio"].nunique() < 3:
        return {"error": "Se necesitan pruebas con al menos 3 precios distintos para estimar la elasticidad."}

    # 4. La pendiente de ln(unidades) contra ln(precio) es la elasticidad
    eps = float(np.polyfit(COMPLETAR, COMPLETAR, 1)[0])    # pista: np.log(df["precio"]), np.log(df["unidades"])

    if eps < -1:
        lectura = "elástica: las ventas reaccionan más que el precio"
    elif eps < 0:
        lectura = "inelástica: las ventas reaccionan menos que el precio"
    else:
        lectura = "positiva: revisen los datos, no es lo normal"
    return {"segmento": segmento or "todos", "elasticidad": round(eps, 2),
            "pruebas_usadas": int(len(df)), "lectura": lectura}

def proponer_precio(precio_actual: float, costo: float, elasticidad: float, unidades_actuales: float) -> dict:
    """Precio óptimo P* = C × ε ÷ (1 + ε) y precio propuesto respetando las reglas de la empresa:
    cambio máximo de ±10% por ciclo, precio de al menos 1.2 × costo, y si el cambio supera 5%
    necesita APROBACIÓN HUMANA. Devuelve la utilidad mensual de hoy y la de la propuesta.
    precio_actual (US$), costo por unidad o cliente (US$), elasticidad (negativa, por ejemplo -1.4),
    unidades_actuales: unidades vendidas al mes hoy."""
    p, C, e, Q = precio_actual, costo, elasticidad, unidades_actuales
    # Barandas de datos
    if p <= 0 or C <= 0 or Q <= 0:
        return {"error": "Precio, costo y unidades deben ser mayores que 0."}
    if COMPLETAR:                                     # pista: e >= 0  (la elasticidad debe ser negativa)
        return {"error": "La elasticidad debe ser negativa (si sube el precio, se vende menos). Revisa el signo."}
    # Precio óptimo (solo existe si la demanda es elástica, ε < −1)
    if e < -1:
        p_optimo = COMPLETAR                          # pista: C × e ÷ (1 + e)
    else:
        p_optimo = None
    # Reglas de la empresa
    propuesto = p * 1.10 if p_optimo is None else p_optimo
    propuesto = min(propuesto, COMPLETAR)             # pista: tope de subir máximo 10% → p × 1.10
    propuesto = max(propuesto, p * 0.90)        # tope: bajar máximo 10%
    propuesto = max(propuesto, COMPLETAR)             # pista: margen mínimo → 1.2 × C
    cambio = propuesto / p - 1

    def utilidad(precio):
        return (precio - C) * Q * (precio / p) ** e

    return {"precio_optimo": round(p_optimo, 2) if p_optimo else "no hay óptimo: con ε entre -1 y 0 conviene subir hasta el tope",
            "precio_propuesto": round(propuesto, 2), "cambio_pct": round(cambio * 100, 1),
            "utilidad_mensual_hoy": round(utilidad(p)), "utilidad_mensual_propuesta": round(utilidad(propuesto)),
            "requiere_aprobacion_humana": COMPLETAR}  # pista: abs(cambio) > 0.05

def metricas_regla_asociacion(producto_a: str, producto_b: str, fuente: str = "tickets") -> dict:
    """Soporte, confianza y lift de la regla A → B (Apriori, venta cruzada), calculados con los
    tickets de la fuente de datos. Lift mayor que 1 = quien compra A compra B más de lo normal.
    producto_a, producto_b: nombres de los productos (como aparecen en los datos).
    fuente: nombre de la fuente de tickets (por defecto "tickets")."""
    # 1. Leer los datos
    try:
        df = cargar_datos(fuente)
    except ValueError as e:
        return {"error": str(e)}

    # 2. Baranda: los productos tienen que existir (si no, sugerimos nombres parecidos)
    productos = sorted(df["producto"].astype(str).unique())
    for nombre in (producto_a, producto_b):
        if nombre not in productos:
            parecidos = difflib.get_close_matches(nombre, productos, n=5, cutoff=0.3)
            return {"error": f"No existe el producto '{nombre}'.", "quizas_quisiste_decir": parecidos}
    if producto_a == producto_b:
        return {"error": "A y B deben ser productos distintos."}

    # 3. Cada ticket → el conjunto de productos que tiene
    canastas = df.groupby("ticket")["producto"].apply(set)
    n = len(canastas)
    con_a = canastas.apply(lambda s: producto_a in s)       # True si el ticket tiene A
    con_b = canastas.apply(lambda s: producto_b in s)       # True si el ticket tiene B

    # 4. Las tres fórmulas
    soporte_a = con_a.sum() / n
    soporte_b = con_b.sum() / n
    soporte_ab = COMPLETAR                            # pista: (con_a & con_b).sum() ÷ n
    confianza = COMPLETAR                             # pista: soporte_ab ÷ soporte_a
    lift = COMPLETAR                                  # pista: confianza ÷ soporte_b
    return {"tickets": int(n), "soporte_a": round(float(soporte_a), 4), "soporte_b": round(float(soporte_b), 4),
            "soporte_ab": round(float(soporte_ab), 4), "confianza": round(float(confianza), 4), "lift": round(float(lift), 2),
            "lectura": "vale la pena recomendar B a quien compra A" if lift > 1 else "no se compran juntos más de lo normal"}

def segmentar_clientes(k: int, fuente: str = "clientes") -> dict:
    """Agrupa a los clientes de la fuente de datos en k segmentos con k-means, usando las
    variables numéricas definidas en FUENTES (estandarizadas). Devuelve, por segmento: número
    de clientes, % de clientes, % del gasto total y el promedio de cada variable.
    k: número de segmentos (entre 2 y 6). fuente: nombre de la fuente (por defecto "clientes")."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    # 1. Leer los datos
    try:
        df = cargar_datos(fuente)
    except ValueError as e:
        return {"error": str(e)}

    # 2. Barandas: k razonable y al menos 2 variables
    if COMPLETAR:                                     # pista: k < 2 or k > 6
        return {"error": "k debe estar entre 2 y 6 segmentos."}
    variables = FUENTES[fuente].get("variables", [])
    if len(variables) < 2:
        return {"error": f"Definan al menos 2 'variables' numéricas en FUENTES['{fuente}']."}

    # 3. Estandarizar (misma escala para todas) y correr k-means
    datos = df[variables].dropna()
    X = StandardScaler().fit_transform(datos)
    etiquetas = KMeans(n_clusters=int(k), n_init=10, random_state=0).fit_predict(COMPLETAR)   # pista: X
    datos = datos.assign(segmento=etiquetas)

    # 4. Resumen por segmento
    gasto = df.loc[datos.index, "gasto"] if "gasto" in df.columns else None
    segmentos = []
    for s, grupo in datos.groupby("segmento"):
        fila = {"clientes": int(len(grupo)), "pct_clientes": round(len(grupo) / len(datos) * 100, 1)}
        if gasto is not None:
            fila["pct_gasto"] = round(float(gasto[grupo.index].sum() / gasto.sum() * 100), 1)
        fila["promedios"] = {v: round(float(grupo[v].mean()), 1) for v in variables}
        segmentos.append(fila)
    segmentos.sort(key=lambda f: f.get("pct_gasto", 0), reverse=True)
    for i, fila in enumerate(segmentos, 1):
        fila["segmento"] = f"S{i}"
    return {"k": int(k), "clientes_usados": int(len(datos)), "segmentos": segmentos,
            "nota": "ordenados de mayor a menor % del gasto"}

def _sin_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")


def buscar_apunte(tema: str) -> dict:
    """Busca en los apuntes del curso de Marketing Analytics (carpeta CARPETA_APUNTES) y devuelve
    los párrafos más relacionados con el tema, con el nombre del archivo de donde salen.
    Úsala ANTES de explicar un concepto o una fórmula del curso.
    tema: palabras clave, por ejemplo "uplift grupo de control" o "precio óptimo"."""
    # 1. Buscar los archivos de apuntes
    archivos = sorted(glob.glob(os.path.join(CARPETA_APUNTES, "*.md")) + glob.glob(os.path.join(CARPETA_APUNTES, "*.txt")))
    if not archivos:
        return {"error": f"No encontré apuntes en la carpeta '{CARPETA_APUNTES}'."}

    # 2. Separar el tema en palabras clave (sin acentos, de 3 letras o más)
    palabras = [p for p in re.findall(r"\w+", _sin_acentos(tema)) if len(p) >= 3]
    if not palabras:
        return {"error": "Escribe al menos una palabra clave de 3 letras o más."}

    # 3. Darle puntos a cada párrafo según cuántas veces aparecen las palabras
    resultados = []
    for ruta in archivos:
        texto = open(ruta, encoding="utf-8").read()
        for parrafo in re.split(r"\n\s*\n", texto):             # un párrafo = un pedazo (chunk)
            puntos = sum(_sin_acentos(parrafo).count(p) for p in COMPLETAR)   # pista: palabras
            if puntos > 0:
                resultados.append((puntos, os.path.basename(ruta), parrafo.strip()[:600]))

    # 4. Devolver los 3 párrafos con más puntos, con su archivo (la "cita")
    if not resultados:
        return {"aviso": "No encontré nada sobre ese tema en los apuntes.", "archivos": [os.path.basename(a) for a in archivos]}
    resultados.sort(reverse=True)
    return {"resultados": [{"archivo": a, "texto": t} for _, a, t in resultados[:COMPLETAR]]}   # pista: 3

# ============================================================ 5. El agente

HERRAMIENTAS = {
    "listar_fuentes": listar_fuentes,
    "calcular_clv": calcular_clv,
    "churn_maximo_tolerable": churn_maximo_tolerable,
    "valor_campana_retencion": valor_campana_retencion,
}

INSTRUCCIONES = """Eres un tutor experto en Marketing Analytics para estudiantes de maestría.
1. Para cualquier número, usa una herramienta. Nunca calcules de memoria.
2. Si falta un dato, pregunta; no lo supongas.
3. Si una herramienta devuelve un error, explícaselo al usuario y pide el dato correcto.
4. Si no sabes qué segmento, producto o fuente de datos existe, usa listar_fuentes.
5. Antes de explicar un concepto del curso, usa buscar_apunte y cita el archivo.
6. Si una propuesta de precio dice requiere_aprobacion_humana, dilo claramente: una persona debe aprobarla.
7. Explica en pasos cortos, muestra la fórmula y define cada sigla."""


def llamar_gemini(contenido, config=None):
    """Llama a Gemini. Si nos pasamos del límite gratuito (error 429), espera 40 segundos y reintenta."""
    for intento in range(4):
        try:
            return client.models.generate_content(model=MODELO, contents=contenido, config=config)
        except errors.ClientError as e:
            if e.code == 429 and intento < 3:
                print("Límite de Gemini (15 llamadas por minuto). Espero 40 segundos...")
                time.sleep(40)
            else:
                raise


def preguntar(pregunta, historial=None, max_pasos=8, mostrar=True, herramientas=None):
    """Le hace una pregunta al agente. Devuelve (respuesta, historial, pasos).
    pasos = lista de herramientas que usó, para verificar sus cuentas.
    herramientas = menú a usar (si no se da, usa todo HERRAMIENTAS)."""
    menu = herramientas if herramientas is not None else HERRAMIENTAS
    config = types.GenerateContentConfig(
        system_instruction=INSTRUCCIONES,
        tools=list(menu.values()),
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
    historial = list(historial or [])
    historial.append(types.Content(role="user", parts=[types.Part.from_text(text=pregunta)]))
    pasos = []

    for paso in range(1, max_pasos + 1):
        r = llamar_gemini(historial, config)                # 1. el LLM piensa
        historial.append(r.candidates[0].content)
        if not r.function_calls:                             # 2. sin herramientas = terminó
            return r.text, historial, pasos
        resultados = []
        for pedido in r.function_calls:                      # 3. ejecutamos lo que pidió
            datos = dict(pedido.args)
            try:
                salida = menu[pedido.name](**datos)
            except Exception as e:                           # baranda: no se cae, le avisa al LLM
                salida = {"error": f"{type(e).__name__}: {e}"}
            pasos.append({"herramienta": pedido.name, "datos": datos, "resultado": salida})
            if mostrar:
                print(f"Paso {paso}: {pedido.name}({datos}) → {str(salida)[:160]}")
            resultados.append(types.Part.from_function_response(name=pedido.name,
                                                                response={"resultado": salida}))
        historial.append(types.Content(role="user", parts=resultados))   # 4. le devolvemos todo
    return "Me detuve: llegué al máximo de pasos.", historial, pasos


def revisar(descripcion, obtenido, esperado, tolerancia=0.01):
    """Compara el resultado de una herramienta con el ejemplo resuelto a mano."""
    if isinstance(obtenido, (int, float)) and abs(obtenido - esperado) <= tolerancia * max(1, abs(esperado)):
        print("OK      ", descripcion, "→", obtenido)
    else:
        print("REVISAR ", descripcion, "→ obtuvo", obtenido, "· esperado", esperado)

# El menú completo: nombre que pide el LLM → función de Python
HERRAMIENTAS.update({
    "relacion_clv_cac": relacion_clv_cac,
    "estimar_elasticidad": estimar_elasticidad,
    "proponer_precio": proponer_precio,
    "metricas_regla_asociacion": metricas_regla_asociacion,
    "segmentar_clientes": segmentar_clientes,
    "buscar_apunte": buscar_apunte,
})
