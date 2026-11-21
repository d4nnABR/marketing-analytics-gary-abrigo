# Semana 9 · Laboratorio: agente con churn y uplift

Marketing Analytics

Laboratorio: Ampliación del agente con churn y uplift

Pregunta guía: ¿cómo le enseño a mi agente dos herramientas nuevas del curso, y cómo compruebo que sus respuestas son correctas?

## Instrucciones

En la demo vieron un agente con una sola herramienta: calcular_clv. Hoy cada equipo le agrega dos herramientas más del toolkit del curso y comprueba que el agente las usa bien.

|  | Herramienta | Tema del curso | Pregunta de negocio que responde |
| Ya viene | calcular_clv | CLV (Customer Lifetime Value) | ¿Cuánto vale un cliente? |
| Hoy | churn_maximo_tolerable | Churn y pricing | Si subo el precio, ¿cuánto churn aguanto sin perder valor? |
| Hoy | valor_campana_retencion | Uplift (Actividad 2) | ¿Vale la pena esta campaña de retención? |

## Materiales

Laboratorio_Agente_Churn_Uplift.ipynb: el notebook donde van a trabajar, con el paso a paso de cada herramienta, igual que en la demo del CLV. Ya trae la conexión con Gemini, calcular_clv y el ciclo del agente (Parte 0). En cada herramienta ustedes completan los espacios ___ guiados por pistas; si se traban, cada parte tiene la solución escondida (ábranla solo después de intentarlo).

Configuración: la misma de la demo. En VS Code: entorno virtual (.venv), pip install google-genai python-dotenv ipykernel y el archivo .env con su GEMINI_API_KEY. En Colab: la llave en Secrets.

## Antes de empezar: su llave de Gemini (API key)

La API key (Application Programming Interface key) es la clave que deja a su código hablar con Gemini. Es gratis y se crea una sola vez; si ya la crearon en la demo, sáltense esta parte.

1. Entren a aistudio.google.com e inicien sesión con su cuenta de Google. Si su cuenta de la universidad no los deja entrar, usen una cuenta personal de Gmail. Acepten los términos si es la primera vez.

2. Abajo a la izquierda, hagan clic en el ícono de llave (Get API key).

Figura 1. Google AI Studio: el ícono de llave (Get API key), abajo a la izquierda.

3. Hagan clic en Create API key. Si les pide un proyecto, elijan el que aparece o creen uno nuevo; el nombre no importa.

4. Abran la llave y usen el botón Copiar clave. Las llaves nuevas empiezan con AQ. y las antiguas con AIza; las dos sirven.

Figura 2. Detalles de la clave de API. La llave está tapada a propósito: nunca la muestren en pantalla.

5. Guárdenla fuera del código:

| Dónde trabajan | Qué hacer |
| VS Code | Creen un archivo llamado exactamente .env (con punto al inicio y sin .txt) en la carpeta del notebook, con una sola línea: GEMINI_API_KEY=AQ.su_llave (sin comillas ni espacios) |
| Colab | Menú izquierdo → ícono de llave (Secrets) → Add new secret. Name: GEMINI_API_KEY · Value: su llave · activen Notebook access |

Cuidado: nunca peguen la llave dentro del código, en un chat ni en GitHub (agreguen .env al .gitignore). Si se les escapa, bórrenla en AI Studio (Borrar clave) y creen otra. En Colab, userdata.get("GEMINI_API_KEY") recibe el nombre del secreto, no la llave. El plan gratuito permite unas 15 llamadas por minuto.

## La receta para cada herramienta

Cada herramienta sigue los mismos seis pasos (x = número de la parte: 1 o 2):

| Paso | Qué hacen | Dónde |
| 1 | Entender la pregunta de negocio y la fórmula | Paso x.1 |
| 2 | Resolver un ejemplo a mano (el notebook trae una celda "calculadora") | Paso x.2 |
| 3 | Escribir la función: docstring (lo que lee el LLM) y barandas (validaciones), llenando los ___ | Paso x.3 |
| 4 | Probarla sola y comparar con el ejemplo a mano: todo debe salir OK | Paso x.4 |
| 5 | Agregarla al menú HERRAMIENTAS y preguntarle al agente (líneas "Paso 1: …") | Paso x.5 |
| 6 | Trampa: ¿el agente se deja engañar? | Paso x.6 |

Pueden usar IA (ChatGPT, Copilot, Cursor, Gemini) para escribir el código. Lo importante es que sepan si el resultado es correcto y por qué. Por eso el paso 1 va antes que el paso 2: sin el ejemplo a mano no tienen con qué comparar lo que escribió la IA.

## Herramienta 2 · churn_maximo_tolerable

La pregunta: si subo el precio, el margen por cliente sube, pero algunos clientes se van. ¿Cuál es el churn máximo que aguanto sin que baje el CLV?

Fórmula: c' = (m' − CLV × d) ÷ (m' + CLV)

c': churn mensual máximo tolerable (lo que buscamos).

m': margen mensual nuevo por cliente, con el precio nuevo (US$).

CLV: valor de vida del cliente de hoy (US$).

d: 0.008, la tasa de descuento mensual del curso (0.8%).

Ejemplo a mano: hoy el CLV es US$500 y con el precio nuevo el margen pasa a US$28.

| Paso | Cuenta | Resultado |
| Arriba | 28 − 500 × 0.008 = 28 − 4 | 24 |
| Abajo | 28 + 500 | 528 |
| c' | 24 ÷ 528 | 0.0455 = 4.55% |

Lectura: si después del aumento el churn mensual pasa de 4.55%, el aumento de precio destruye valor.

Comprobación: con m = 28 y c = 0.0455, calcular_clv da US$500, igual que antes. Así saben que la fórmula está bien.

Barandas que debe tener: el margen nuevo y el CLV deben ser positivos; y si el margen nuevo es menor que CLV × 0.008, el resultado sale negativo, porque ningún churn mantiene el CLV. En ese caso, devuelvan un error que lo explique (prueba: margen nuevo 3, CLV 500).

Segundo ejemplo (paso 1.4): margen nuevo US$10 y CLV US$200 → c' = (10 − 1.6) ÷ 210 = 0.04 = 4%.

## Herramienta 3 · valor_campana_retencion

La pregunta: ¿vale la pena una campaña de retención?

La clave, de la Actividad 2: el uplift es el efecto incremental: cuántos clientes se quedan gracias a la campaña, comparando contra un grupo de control. No es "el porcentaje que se quedó", porque muchos se habrían quedado igual.

| Concepto | Fórmula |
| Clientes retenidos extra | clientes contactados × uplift |
| Valor generado | retenidos extra × CLV |
| Costo total | clientes contactados × costo por contacto |
| Beneficio neto | valor generado − costo total |
| Uplift mínimo para no perder | costo por contacto ÷ CLV |

Ejemplo a mano: 1,000 clientes, uplift 5%, CLV US$500 y US$10 por contacto.

| Concepto | Cuenta | Resultado |
| Retenidos extra | 1,000 × 0.05 | 50 |
| Valor generado | 50 × 500 | US$25,000 |
| Costo total | 1,000 × 10 | US$10,000 |
| Beneficio neto | 25,000 − 10,000 | US$15,000 → conviene |
| Uplift mínimo | 10 ÷ 500 | 2% |

Segundo ejemplo (paso 2.4): 2,000 clientes, uplift 1%, CLV US$300 y US$5 por contacto → beneficio neto de −US$4,000: no conviene (el uplift mínimo es 1.67%).

Baranda que debe tener: el uplift debe estar entre 0 y 1. Si alguien escribe 5, el agente debe preguntar si quiso decir 5% (0.05).

## Probarlo con el agente

Al final (Parte 3) corren todas las preguntas de una vez con evaluar(). El banco ya trae 5 preguntas con respuesta conocida y 3 trampas:

| Trampa | Qué debe hacer el agente |
| ¿Cuánto vale un cliente si el churn es 4%? | Preguntar el margen, no inventarlo |
| Margen US$25 y churn de 120%. ¿CLV? | Decir que es imposible (no se puede perder más del 100%) |
| Contacté a 1,000 clientes y el 30% se quedó. Con CLV de US$500, ¿cuánto ganó la campaña? | Explicar que 30% no es uplift y pedir el grupo de control |

Las trampas se revisan a ojo. Si el agente cae en una, no lo escondan: anótenlo, mejoren el docstring, las instrucciones o la baranda, y vuelvan a probar. Esa iteración es la parte más importante del laboratorio.

Agreguen 1 trampa propia al BANCO, pensada para sus herramientas. Ideas: un uplift de 5 en lugar de 0.05, un margen nuevo menor al actual, o una pregunta que mezcle meses y años.

## Entregable del avance (al final de la clase)

El notebook con churn_maximo_tolerable y valor_campana_retencion funcionando: los pasos 1.4 y 2.4 en OK y las trampas 1.6 y 2.6 probadas.

El resultado de evaluar(): cuántas de las 5 preguntas con respuesta conocida acierta, y qué pasó con cada trampa.

1 trampa propia agregada al BANCO, con lo que hizo el agente.

Una nota al final del notebook: en qué trampa cayó el agente y qué cambiaron para arreglarlo.

Súbanlo a su rama de GitHub del grupo, igual que las actividades anteriores.

## Si algo falla

| Lo que ven | Qué hacer |
| REVISAR en los pasos x.4 | Comparen paso por paso con el ejemplo a mano: revisen d = 0.008 (no 0.08) y los paréntesis de la fórmula |
| El agente no usa su herramienta nueva | Revisen que corrieron el paso x.5 (la línea HERRAMIENTAS[...] = ...). Mejoren el docstring: es lo único que el LLM sabe de ella |
| El agente calcula de memoria | Revisen la regla 1 de INSTRUCCIONES; mejoren el docstring o agreguen una baranda (el prompt solo pide; el código obliga) |
| NameError: name '___' is not defined | Falta llenar un espacio ___ en esa celda |
| SecretNotFoundError (Colab) | Pegaron la llave dentro de userdata.get(). Va el nombre: userdata.get("GEMINI_API_KEY") |
| API key not valid | Revisen que el .env tenga la llave completa, sin comillas ni espacios, y que esté guardado |
| Error 429 | Límite gratuito de Gemini (15 llamadas por minuto). El código espera 40 segundos solo; si se repite, esperen un minuto |
