import re
import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from afinn import Afinn

# --- CONFIGURACIÓN ---
# Rutas a los archivos de las canciones
ruta_cancion1 = os.path.join(os.path.dirname(__file__), 'cancion1.txt')
ruta_cancion2 = os.path.join(os.path.dirname(__file__), 'cancion2.txt')

# Ruta al léxico AFINN
ruta_lexico = os.path.join(os.path.dirname(__file__), 'lexico_afinn.csv')


# --- CARGAR ARCHIVOS ---
def cargar_archivo(ruta):
    """Carga el contenido de un archivo de texto"""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {ruta}")
        return None


# Cargar ambas canciones
cancion1 = cargar_archivo(ruta_cancion1)
cancion2 = cargar_archivo(ruta_cancion2)

if not cancion1 or not cancion2:
    print("❌ No se pudieron cargar ambas canciones. Verifica que existan los archivos.")
    exit(1)

# --- PROCESAMIENTO ---
# Lista de stopwords comunes en español
stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es',
    'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo',
    'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi',
    'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])


def procesar_y_contar(text, stopwords=None):
    """Normaliza, tokeniza y cuenta palabras"""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    if stopwords:
        words = [word for word in words if word not in stopwords]
    return Counter(words)


# Procesar ambas canciones
contador1 = procesar_y_contar(cancion1, stopwords=stopwords_es)
contador2 = procesar_y_contar(cancion2, stopwords=stopwords_es)


# --- ANÁLISIS DE FRECUENCIAS ---
def mostrar_top_palabras(contador, titulo, n=10):
    """Muestra y devuelve las n palabras más frecuentes"""
    print(f"\n--- {titulo} ---")
    top_palabras = contador.most_common(n)
    for palabra, frecuencia in top_palabras:
        print(f"{palabra}: {frecuencia}")
    return top_palabras


# Obtener top palabras para ambas canciones
top1 = mostrar_top_palabras(contador1, "Top 10 Palabras Canción 1")
top2 = mostrar_top_palabras(contador2, "Top 10 Palabras Canción 2")


# --- VISUALIZACIÓN COMPARATIVA ---
def graficar_comparacion(top1, top2, titulo1, titulo2):
    """Genera gráfico comparativo de top palabras"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Gráfico 1
    palabras1, frecuencias1 = zip(*top1)
    ax1.bar(palabras1, frecuencias1, color='skyblue')
    ax1.set_title(f'Top Palabras {titulo1}', fontsize=14)
    ax1.set_xlabel('Palabras')
    ax1.set_ylabel('Frecuencia')
    ax1.tick_params(axis='x', rotation=45)

    # Gráfico 2
    palabras2, frecuencias2 = zip(*top2)
    ax2.bar(palabras2, frecuencias2, color='salmon')
    ax2.set_title(f'Top Palabras {titulo2}', fontsize=14)
    ax2.set_xlabel('Palabras')
    ax2.tick_params(axis='x', rotation=45)

    plt.suptitle('Comparación de Palabras Clave', fontsize=18)
    plt.tight_layout()
    plt.show()


graficar_comparacion(top1, top2, "Canción 1", "Canción 2")

# --- ANÁLISIS DE SENTIMIENTO ---
# Cargar léxico AFINN
try:
    lexico = pd.read_csv(ruta_lexico, encoding='utf-8')
    col_palabra = lexico.columns[0]
    col_puntuacion = lexico.columns[1]

    # Filtrar palabras positivas y negativas
    positivas = lexico[lexico[col_puntuacion] > 0][col_palabra].tolist()
    negativas = lexico[lexico[col_puntuacion] < 0][col_palabra].tolist()

    print(f"\n✅ Léxico cargado: {len(positivas)} palabras positivas, {len(negativas)} palabras negativas")
except Exception as e:
    print(f"❌ Error al cargar el léxico: {e}")
    exit(1)


def analizar_sentimiento(texto, stopwords, positivas, negativas):
    """Analiza el sentimiento de un texto completo"""
    texto_lower = texto.lower()
    palabras = re.findall(r'\b\w+\b', texto_lower)
    palabras_limpio = [p for p in palabras if p not in stopwords]

    # Contar palabras positivas y negativas
    score_pos = sum(1 for p in palabras_limpio if p in positivas)
    score_neg = sum(1 for p in palabras_limpio if p in negativas)

    # Calcular puntaje final
    puntaje = score_pos - score_neg

    # Clasificación
    if puntaje > 0:
        clasificacion = "Positivo"
    elif puntaje < 0:
        clasificacion = "Negativo"
    else:
        clasificacion = "Neutro"

    return {
        "puntaje": puntaje,
        "clasificacion": clasificacion,
        "palabras_positivas": [p for p in palabras_limpio if p in positivas],
        "palabras_negativas": [p for p in palabras_limpio if p in negativas]
    }


# Analizar sentimiento de ambas canciones
resultado1 = analizar_sentimiento(cancion1, stopwords_es, positivas, negativas)
resultado2 = analizar_sentimiento(cancion2, stopwords_es, positivas, negativas)


# --- VISUALIZACIÓN DE SENTIMIENTO ---
def graficar_sentimiento(resultado1, resultado2, titulo1, titulo2):
    """Genera gráfico comparativo de sentimiento"""
    labels = ['Positivo', 'Negativo', 'Neutro']
    sizes1 = [len(resultado1['palabras_positivas']),
              len(resultado1['palabras_negativas']),
              0 if resultado1['clasificacion'] != 'Neutro' else 1]

    sizes2 = [len(resultado2['palabras_positivas']),
              len(resultado2['palabras_negativas']),
              0 if resultado2['clasificacion'] != 'Neutro' else 1]

    # Crear gráfico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Gráfico 1
    ax1.pie(sizes1, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=['#99ff99', '#ff9999', '#cccccc'], textprops={'fontsize': 12})
    ax1.set_title(f'Sentimiento {titulo1}', fontsize=14)

    # Gráfico 2
    ax2.pie(sizes2, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=['#99ff99', '#ff9999', '#cccccc'], textprops={'fontsize': 12})
    ax2.set_title(f'Sentimiento {titulo2}', fontsize=14)

    plt.tight_layout()
    plt.show()


graficar_sentimiento(resultado1, resultado2, "Canción 1", "Canción 2")

# --- RESULTADOS FINALES ---
print("\n--- RESULTADOS FINALES ---")
print(f"Canción 1: Puntaje {resultado1['puntaje']} ({resultado1['clasificacion']})")
print(f"Canción 2: Puntaje {resultado2['puntaje']} ({resultado2['clasificacion']})")

print("\nPalabras positivas en Canción 1:", resultado1['palabras_positivas'][:5])
print("Palabras negativas en Canción 1:", resultado1['palabras_negativas'][:5])
print("\nPalabras positivas en Canción 2:", resultado2['palabras_positivas'][:5])
print("Palabras negativas en Canción 2:", resultado2['palabras_negativas'][:5])
