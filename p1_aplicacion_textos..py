import re
import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from afinn import Afinn

# --- NUESTRO CORPUS (BASE DE DATOS DE TEXTO) ---
# --- LEER EL CORPUS DESDE UN ARCHIVO TXT ---
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(script_dir, 'corpus.txt')  # Cambia 'corpus.txt' por el nombre de tu archivo

try:
    with open(txt_path, 'r', encoding='utf-8') as f:
        corpus = [f.read()]  # Lee todo el archivo como una sola cadena
    print(f"✅ Corpus cargado desde '{txt_path}'")
except FileNotFoundError:
    print(f"❌ No se encontró el archivo 'corpus.txt' en la carpeta del script.")
    exit(1)

# --- PROCESAMIENTO ---

# 1. Unificar todo el texto
# Para analizar la frecuencia en todo el corpus, primero unimos todas las frases en un único bloque de texto.
print("Paso 1: Unificando el corpus en un solo bloque de texto...")
all_text = ' '.join(corpus)
print(f"Texto completo: '{all_text[:100]}...'")

# 2. Normalización: Convertir a minúsculas
# Esto es crucial para que palabras como "Fantástico" y "fantástico" se cuenten como una sola.
print("\nPaso 2: Normalizando el texto a minúsculas...")
all_text_lower = all_text.lower()
print(f"Texto normalizado: '{all_text_lower[:100]}...'")

# 3. Tokenización: Dividir el texto en palabras (tokens)
# Usamos una expresión regular `\b\w+\b` que es más robusta que un simple `.split()`.
# `\b` asegura que solo cojamos palabras completas, ignorando signos de puntuación como comas o puntos.
print(""
      "\nPaso 3: Tokenizando el texto en palabras...")
words = re.findall(r'\b\w+\b', all_text_lower)
print(f"Primeras 20 palabras (tokens): {words[:20]}")

# 4. Conteo de Frecuencias
# `collections.Counter` es una herramienta de Python extremadamente eficiente para contar la frecuencia de elementos en una lista.
print("\nPaso 4: Contando la frecuencia de cada palabra...")
word_counts = Counter(words)

# `most_common(10)` nos da una lista de las 10 tuplas (palabra, frecuencia) más comunes.
top_10_words = word_counts.most_common(10)

print("\n--- RESULTADOS DEL ANÁLISIS DE FRECUENCIA ---")
print("Top 10 palabras más frecuentes (antes de la limpieza):")
for word, count in top_10_words:
    print(f"- '{word}': {count} veces")

# --- VISUALIZACIÓN ---
# Un análisis no está completo si no podemos comunicarlo visualmente.

print("\nGenerando gráfico de barras... (una ventana nueva debería aparecer)")

# Desempaquetamos las palabras y sus conteos en dos listas separadas para el gráfico.
words_for_plot, counts_for_plot = zip(*top_10_words)

# Creamos la figura y los ejes para el gráfico.
plt.figure(figsize=(12, 7))
plt.bar(words_for_plot, counts_for_plot, color='skyblue')

# Añadimos títulos y etiquetas para que el gráfico sea legible.
plt.title('Top 10 Palabras Más Frecuentes en el Corpus (Sin Limpieza)')
plt.xlabel('Palabras')
plt.ylabel('Frecuencia')
plt.xticks(rotation=45, ha="right") # Rotamos las etiquetas para que no se solapen
plt.tight_layout() # Ajusta el gráfico para que todo quepa bien

# Mostramos el gráfico. Esto abrirá una nueva ventana.
plt.show()

#Lista de stopwords comunes en español. En proyectos reales, se usan listas más exhaustivas de librerías como NLTK o spaCy.
stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

# --- PROCESAMIENTO ---

# Función para procesar y limpiar texto
def procesar_y_contar(text, stopwords=None):
    """Toma un bloque de texto, lo normaliza, tokeniza y opcionalmente elimina stopwords."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    if stopwords:
        words = [word for word in words if word not in stopwords]
    return Counter(words)

# 1. Análisis SIN limpieza (Repetimos el paso del ejercicio 1 para comparar)
print("Paso 1: Analizando frecuencias SIN limpiar el texto...")
all_text = ' '.join(corpus)
word_counts_sin_limpieza = procesar_y_contar(all_text)
top_10_sin_limpieza = word_counts_sin_limpieza.most_common(10)
print("Top 10 palabras (sin limpieza):", top_10_sin_limpieza)

# 2. Análisis CON limpieza
print("\nPaso 2: Analizando frecuencias CON limpieza de stopwords...")
word_counts_con_limpieza = procesar_y_contar(all_text, stopwords=stopwords_es)
top_10_con_limpieza = word_counts_con_limpieza.most_common(10)
print("Top 10 palabras (con limpieza):", top_10_con_limpieza)


# --- VISUALIZACIÓN COMPARATIVA ---

print("\nGenerando gráficos comparativos...")

# Desempaquetamos los resultados para ambos gráficos
words_sin, counts_sin = zip(*top_10_sin_limpieza)
words_con, counts_con = zip(*top_10_con_limpieza)

# Creamos una figura con dos subplots (uno al lado del otro)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Gráfico 1: Sin Limpieza
ax1.bar(words_sin, counts_sin, color='#ff9999')
ax1.set_title('Frecuencias ANTES de la Limpieza', fontsize=16)
ax1.set_xlabel('Palabras')
ax1.set_ylabel('Frecuencia')
ax1.tick_params(axis='x', rotation=45)

# Gráfico 2: Con Limpieza
ax2.bar(words_con, counts_con, color='#99ff99')
ax2.set_title('Frecuencias DESPUÉS de la Limpieza', fontsize=16)
ax2.set_xlabel('Palabras')
ax2.tick_params(axis='x', rotation=45)

# Título general para toda la figura
fig.suptitle('Impacto de la Eliminación de Stopwords', fontsize=20)

# Ajustamos el layout y mostramos
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajuste para el supertítulo
plt.show()

print("Observación: ¡El cambio es drástico! El gráfico de la derecha revela las palabras que realmente aportan significado:")
# --- CARGAR EL LÉXICO DESDE EL CSV ---
# Ruta al CSV (ajusta el nombre si es distinto)
csv_path = os.path.join(os.path.dirname(__file__), 'lexico_afinn.csv')

# Cargar el archivo CSV
# Si tu CSV tiene otro separador (por ejemplo ';'), cámbialo con sep=';'
lexico = pd.read_csv(csv_path, encoding='utf-8')

# Si las columnas no tienen nombres estándar, puedes renombrarlas así:
# lexico.columns = ['palabra', 'puntuacion']

# Verifica las primeras filas para confirmar columnas
print("Columnas detectadas:", list(lexico.columns))
print(lexico.head())

# Detectar automáticamente columnas
col_palabra = lexico.columns[0]
col_puntuacion = lexico.columns[1]

# Filtrar palabras positivas y negativas
positivas = lexico[lexico[col_puntuacion] > 0][col_palabra].tolist()
negativas = lexico[lexico[col_puntuacion] < 0][col_palabra].tolist()

# Guardar en archivos TXT
with open('lexico_positivo.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(positivas))

with open('lexico_negativo.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(negativas))

print(f"\n✅ Archivos generados correctamente:")
print(f"  - lexico_positivo.txt ({len(positivas)} palabras)")
print(f"  - lexico_negativo.txt ({len(negativas)} palabras)")

# --- PROCESAMIENTO ---
def analizar_sentimiento(frase, stopwords, positivas, lexico_neg):
    """Analiza una sola frase y devuelve su puntaje y clasificación de sentimiento."""
    # 1. Limpieza (Normalización y eliminación de stopwords)
    frase_lower = frase.lower()
    words = re.findall(r'\b\w+\b', frase_lower)
    words_cleaned = [word for word in words if word not in stopwords]

    # 2. Conteo de palabras positivas y negativas
    score_pos = sum(1 for word in words_cleaned if word in positivas)
    score_neg = sum(1 for word in words_cleaned if word in negativas)

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
        "palabras_clave": [word for word in words_cleaned if word in positivas or word in negativas]
    }


# Analizamos cada frase del corpus
resultados_analisis = [analizar_sentimiento(frase, stopwords_es, positivas,negativas) for frase in corpus]

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


