# Segmentación de clientes

Objetivo: grupos de clientes parecidos entre sí y distintos de los demás, que se puedan atender con acciones diferentes.

Antes de agrupar hay que ESTANDARIZAR: z = (valor − promedio) ÷ desviación estándar. Si no, las variables grandes (ingreso en dólares) dominan a las chicas (visitas al mes).
Ejemplo: ingreso 60,000, promedio 50,000, desviación 20,000 → z = (60,000 − 50,000) ÷ 20,000 = 0.5.

Métodos:
- k-means: asigna cada cliente al centro más cercano; supone grupos redondos y de tamaño parecido; hay que elegir k. Silueta (de −1 a 1): qué tan separados quedan; > 0.5 fuerte, 0.25–0.5 moderada, < 0.25 débil.
- Jerárquico (Ward): une grupos de abajo hacia arriba; el dendrograma muestra dónde cortar.
- DBSCAN: agrupa por densidad; encuentra formas raras y marca "ruido"; muy sensible al parámetro eps.
- GMM (mezclas gaussianas): grupos en forma de elipse y probabilidad de pertenencia a cada grupo.
- k-prototypes: mezcla variables numéricas y categóricas (por ejemplo, estado civil).

Cómo leer un segmento: % de clientes vs % del gasto. Índice de valor = % del gasto ÷ % de clientes.
Ejemplo: un segmento con 20% de los clientes y 40% del gasto tiene índice 40 ÷ 20 = 2.0 (vale el doble de su peso).
Un segmento útil es medible, de tamaño suficiente, accesible, diferenciado y accionable. Recalcular la segmentación periódicamente (por ejemplo, cada trimestre).
