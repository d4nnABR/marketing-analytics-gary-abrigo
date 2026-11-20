import inspect, re, time, unicodedata
from google import genai
from google.genai import types, errors
from herramientas_agovalle import HERRAMIENTAS as H_AGOVALLE
from herramientas_gary import HERRAMIENTAS as H_GARY

HERRAMIENTAS = {**H_AGOVALLE, **H_GARY}

MAX_CHARS = 300
MAX_PREGUNTAS = 15
MAX_PASOS = 6
MAX_HISTORIAL = 4

FUERA_DE_TEMA = ("Solo respondo preguntas de los temas del curso: CLV, RFM, churn, uplift, "
                 "recomendación, CAC, segmentación y precios.")

PALABRAS = [
    "clv", "valor de vida", "ltv", "cliente", "margen", "rfm", "recencia", "frecuencia", "bg/nbd",
    "churn", "retencion", "cancel", "fuga", "uplift", "campana", "qini", "control",
    "apriori", "lift", "soporte", "confianza", "regla", "recomend", "canasta", "venta cruzada",
    "cac", "adquisicion", "segment", "k-means", "kmeans", "cluster", "grupo",
    "precio", "elasticidad", "costo", "utilidad", "descuento", "demanda",
]

INSTRUCCIONES = """Eres un tutor experto en Marketing Analytics para estudiantes de maestría.
1. Para cualquier número, usa una herramienta. Nunca calcules de memoria.
2. Si falta un dato, pregunta; no lo supongas (costo, margen, CLV, uplift).
3. Si una herramienta devuelve un error, explícaselo al usuario y pide el dato correcto.
4. Si la pregunta no es de los temas del curso (CLV, RFM, churn, uplift, recomendación, CAC, segmentación, precios), responde solo que no puedes ayudar.
5. Si una herramienta pide aprobación humana, dilo y no lo des por aprobado.
6. Explica en pasos cortos, muestra la fórmula y define cada sigla."""


def normalizar(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def validar(pregunta, usadas):
    """Filtro en código, antes de gastar una llamada al LLM. Devuelve (ok, mensaje)."""
    if usadas >= MAX_PREGUNTAS:
        return False, f"Llegaste al máximo de {MAX_PREGUNTAS} preguntas por sesión."
    if not pregunta.strip():
        return False, "Escribe una pregunta."
    if len(pregunta) > MAX_CHARS:
        return False, f"La pregunta es muy larga (máximo {MAX_CHARS} caracteres)."
    texto = normalizar(pregunta)
    if not any(p in texto for p in PALABRAS):
        return False, FUERA_DE_TEMA
    return True, ""


def crear_cliente(api_key):
    client = genai.Client(api_key=api_key)
    excluir = ("tts", "image", "live", "audio", "embedding", "preview", "exp")
    modelos = []
    for m in client.models.list():
        nombre = m.name.replace("models/", "")
        if "generateContent" in (m.supported_actions or []) and "gemini" in nombre:
            if not any(x in nombre for x in excluir):
                modelos.append(nombre)
    lite = sorted(m for m in modelos if "flash-lite" in m)
    return client, (lite[-1] if lite else sorted(modelos)[-1])


def llamar_llm(client, modelo, contenido, config):
    """Único punto que toca al proveedor: aquí se cambia Gemini por otro."""
    for intento in range(4):
        try:
            return client.models.generate_content(model=modelo, contents=contenido, config=config)
        except (errors.ClientError, errors.ServerError) as e:
            if e.code == 429 and intento < 3:
                time.sleep(40)
            elif e.code == 503 and intento < 3:
                time.sleep(10)
            else:
                raise


def ejecutar(nombre, datos):
    funcion = HERRAMIENTAS.get(nombre)
    if funcion is None:
        return {"error": f"La herramienta {nombre} no existe."}
    validos = inspect.signature(funcion).parameters
    datos = {k: v for k, v in datos.items() if k in validos}
    try:
        return funcion(**datos)
    except Exception as e:
        return {"error": str(e)}


def preguntar(client, modelo, pregunta, historial=None):
    """Devuelve (respuesta, traza). historial: lista de (rol, texto) de turnos anteriores."""
    config = types.GenerateContentConfig(
        system_instruction=INSTRUCCIONES,
        tools=list(HERRAMIENTAS.values()),
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
    contenido = [types.Content(role=rol, parts=[types.Part.from_text(text=t)])
                 for rol, t in (historial or [])[-MAX_HISTORIAL:]]
    contenido.append(types.Content(role="user", parts=[types.Part.from_text(text=pregunta)]))
    traza = []
    for _ in range(MAX_PASOS):
        r = llamar_llm(client, modelo, contenido, config)
        contenido.append(r.candidates[0].content)
        if not r.function_calls:
            return r.text or "", traza
        resultados = []
        for pedido in r.function_calls:
            datos = dict(pedido.args)
            salida = ejecutar(pedido.name, datos)
            traza.append({"herramienta": pedido.name, "datos": datos, "resultado": salida})
            resultados.append(types.Part.from_function_response(
                name=pedido.name, response={"resultado": salida}))
        contenido.append(types.Content(role="user", parts=resultados))
    return "Me detuve: llegué al máximo de pasos.", traza


def numeros_en(texto):
    limpio = re.sub(r"\\[,;! ]|[$\\{}]", "", texto or "")
    encontrados = []
    for n in re.findall(r"-?\d[\d,]*\.?\d*", limpio):
        try:
            encontrados.append(float(n.replace(",", "").rstrip(".")))
        except ValueError:
            pass
    return encontrados


def evaluar_caso(client, modelo, caso):
    """Corre un caso del banco. Devuelve un dict con respuesta, traza y calificación."""
    respuesta, traza = preguntar(client, modelo, caso["pregunta"])
    usadas = [t["herramienta"] for t in traza]
    if caso["esperado"] is None:
        return {"respuesta": respuesta, "traza": traza, "ok": None, "herramienta_ok": None}
    tol = 0.01
    ok = any(abs(n - e) <= tol * max(1, abs(e))
             for e in caso["esperado"] for n in numeros_en(respuesta))
    return {"respuesta": respuesta, "traza": traza, "ok": ok,
            "herramienta_ok": caso.get("herramienta") in usadas}
