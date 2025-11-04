# --- EJERCICIO 3: CLASIFICACIÓN DE SENTIMIENTOS Y VISUALIZACIÓN ---

# --- CONTEXTO ---
# Objetivo: Construir nuestro primer clasificador de sentimientos. Usaremos un método basado en "léxicos",
# que es una de las técnicas más simples e interpretables. También visualizaremos la distribución
# de sentimientos en nuestro corpus para tener una visión general.
#
# ¿Qué es un Léxico de Sentimientos? Es simplemente un diccionario de palabras pre-clasificadas como
# positivas o negativas. Nuestro clasificador asignará un puntaje a cada frase basándose en cuántas
# palabras de cada léxico contiene.

# --- IMPORTACIONES ---
import re
import matplotlib.pyplot as plt
from collections import Counter

# --- CORPUS, STOPWORDS Y LÉXICOS ---
corpus = [
    "Me encanta este producto, es fantástico y muy útil.",
    "El servicio al cliente fue terrible, muy decepcionante.",
    "El precio es adecuado, ni caro ni barato.",
    "No volvería a comprar, la calidad es pésima.",
    "Una experiencia increíble, lo recomiendo totalmente.",
    "El envío tardó más de lo esperado.",
    "Fantástico, simplemente fantástico.",
    "No está mal, pero podría mejorar.", # Frase interesante para analizar
    "La batería dura poquísimo, un desastre."
]

stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

# Léxicos de sentimiento (simplificados)
lexico_positivo = {"encanta", "fantástico", "útil", "adecuado", "increíble", "recomiendo", "totalmente", "mejorar"}
lexico_negativo = {"terrible", "decepcionante", "caro", "barato", "pésima", "tardó", "mal", "poquísimo", "desastre"}

# --- PROCESAMIENTO ---

def analizar_sentimiento(frase, stopwords, lexico_pos, lexico_neg):
    """Analiza una sola frase y devuelve su puntaje y clasificación de sentimiento."""
    # 1. Limpieza (Normalización y eliminación de stopwords)
    frase_lower = frase.lower()
    words = re.findall(r'\b\w+\b', frase_lower)
    words_cleaned = [word for word in words if word not in stopwords]

    # 2. Conteo de palabras positivas y negativas
    score_pos = sum(1 for word in words_cleaned if word in lexico_pos)
    score_neg = sum(1 for word in words_cleaned if word in lexico_neg)

    # 3. Cálculo del puntaje final
    # La lógica más simple: palabras positivas suman 1, negativas restan 1.
    puntaje_final = score_pos - score_neg

    # 4. Clasificación basada en el puntaje
    if puntaje_final > 0:
        clasificacion = "Positiva"
    elif puntaje_final < 0:
        clasificacion = "Negativa"
    else:
        clasificacion = "Neutra"
        
    return {
        "frase": frase,
        "puntaje": puntaje_final,
        "clasificacion": clasificacion,
        "palabras_clave": [word for word in words_cleaned if word in lexico_pos or word in lexico_neg]
    }

# Analizamos cada frase del corpus
resultados_analisis = [analizar_sentimiento(frase, stopwords_es, lexico_positivo, lexico_negativo) for frase in corpus]

print("--- RESULTADOS DEL ANÁLISIS DE SENTIMIENTO ---")
for resultado in resultados_analisis:
    print(f"Frase: '{resultado['frase']}'")
    print(f"  -> Palabras Clave: {resultado['palabras_clave']}")
    print(f"  -> Puntaje: {resultado['puntaje']}, Clasificación: {resultado['clasificacion']}\n")

# Contamos cuántas frases hay de cada categoría para el gráfico
sentiment_counts = Counter([res['clasificacion'] for res in resultados_analisis])
print("\nResumen del Corpus:")
print(sentiment_counts)

# --- VISUALIZACIÓN ---

print("\nGenerando gráfico de tarta...")

# Etiquetas y tamaños para el gráfico
labels = sentiment_counts.keys()
sizes = sentiment_counts.values()
colors = {'Positiva': '#99ff99', 'Negativa': '#ff9999', 'Neutra': '#ffcc99'}

# Aseguramos que los colores coincidan con las etiquetas
color_list = [colors[label] for label in labels]

plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, colors=color_list, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 14})

plt.title('Distribución de Sentimientos en el Corpus', fontsize=16)
plt.axis('equal')  # Asegura que el gráfico de tarta sea un círculo.
plt.show()

print("\n--- FIN DEL EJERCICIO 3 ---")
print("Observación: Nuestro clasificador simple funciona razonablemente bien, pero tiene fallos.")
print("Por ejemplo, 'No está mal' se clasifica como Negativa por la palabra 'mal', ignorando la negación 'No'.")
print("Este es un problema clásico en NLP llamado 'manejo de la negación', que requiere técnicas más avanzadas.")
