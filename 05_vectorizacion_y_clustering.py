# --- EJERCICIO 5: VECTORIZACIÓN Y CLUSTERING DE DOCUMENTOS ---

# --- CONTEXTO ---
# Objetivo: Conectar NLP con Machine Learning. Aprenderemos a convertir texto en vectores numéricos
# significativos (un proceso llamado "vectorización") y luego usaremos un algoritmo de clustering
# (K-Means) para agrupar automáticamente las frases similares. Este es un ejemplo de aprendizaje no supervisado.
#
# ¿Qué es la Vectorización TF-IDF? Es una técnica mucho más sofisticada que el simple conteo de palabras.
# - TF (Term Frequency): Frecuencia de un término. Le da más peso a una palabra si aparece más veces en un documento.
# - IDF (Inverse Document Frequency): Frecuencia Inversa de Documento. Le da más peso a una palabra si es rara
#   en todo el corpus. Penaliza las palabras comunes. 
# El resultado (TF-IDF) es un puntaje que representa la importancia de una palabra para un documento específico.
#
# ¿Qué es PCA? Es una técnica para reducir la dimensionalidad. Nuestros vectores TF-IDF tendrán muchas dimensiones
# (una por cada palabra única). Para poder graficarlos en un plano 2D, usaremos PCA para "comprimirlos" a 2 dimensiones,
# tratando de preservar la mayor cantidad de información posible.

# --- IMPORTACIONES ---
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import re
import numpy as np

# --- CORPUS Y STOPWORDS ---
corpus = [
    "Me encanta este producto, es fantástico y muy útil.",
    "El servicio al cliente fue terrible, muy decepcionante.",
    "El precio es adecuado, ni caro ni barato.",
    "No volvería a comprar, la calidad es pésima.",
    "Una experiencia increíble, lo recomiendo totalmente.",
    "El envío tardó más de lo esperado.",
    "Fantástico, simplemente fantástico.",
    "No está mal, pero podría mejorar.",
    "La batería dura poquísimo, un desastre."
]

stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

# --- PROCESAMIENTO ---

# 1. Limpieza del corpus
# Para scikit-learn, es mejor pasarle una lista de textos limpios.
def limpiar_frase(frase, stopwords):
    frase_lower = frase.lower()
    words = re.findall(r'\b\w+\b', frase_lower)
    words_cleaned = [word for word in words if word not in stopwords]
    return ' '.join(words_cleaned)

print("Paso 1: Limpiando el corpus...")
corpus_limpio = [limpiar_frase(frase, stopwords_es) for frase in corpus]
print("Corpus limpio:", corpus_limpio)

# 2. Vectorización con TF-IDF
# Creamos un objeto TfidfVectorizer. Él se encargará de todo el proceso.
print("\nPaso 2: Vectorizando el corpus con TF-IDF...")
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus_limpio)

# La matriz resultante es una matriz dispersa (sparse matrix) para ahorrar memoria.
print(f"Dimensiones de la matriz TF-IDF: {tfidf_matrix.shape}")
print("(Hay {tfidf_matrix.shape[0]} frases y {tfidf_matrix.shape[1]} palabras únicas en nuestro vocabulario)")

# 3. Clustering con K-Means
# Vamos a pedirle que encuentre 3 grupos (clusters), esperando que se correspondan
# con los sentimientos positivo, negativo y neutro.
print("\nPaso 3: Aplicando K-Means para encontrar 3 clusters...")
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10) # n_init es para estabilidad
kmeans.fit(tfidf_matrix)

# `kmeans.labels_` nos da un array que asigna un número de cluster a cada frase.
clusters = kmeans.labels_

print("Asignación de clusters a cada frase:", clusters)

# Mostramos qué frases cayeron en cada cluster
for i in range(num_clusters):
    print(f"\nCluster {i}:")
    for j, frase in enumerate(corpus):
        if clusters[j] == i:
            print(f"  - '{frase}'")

# 4. Reducción de Dimensionalidad con PCA
# Reducimos la matriz TF-IDF de muchas dimensiones a solo 2 para poder graficarla.
print("\nPaso 4: Reduciendo la dimensionalidad a 2D con PCA...")
pca = PCA(n_components=2, random_state=42)
coordenadas_2d = pca.fit_transform(tfidf_matrix.toarray()) # PCA necesita una matriz densa

print("Coordenadas 2D para cada frase:", np.round(coordenadas_2d, 2))

# --- VISUALIZACIÓN DEL CLUSTERING ---

print("\nGenerando gráfico de dispersión de los clusters...")

plt.figure(figsize=(14, 10))

# Creamos un scatter plot con las coordenadas 2D.
# `c=clusters` le dice a matplotlib que coloree cada punto según el cluster al que pertenece.
scatter = plt.scatter(coordenadas_2d[:, 0], coordenadas_2d[:, 1], c=clusters, cmap='viridis', s=150, alpha=0.8)

# Añadimos etiquetas a cada punto para saber qué frase es.
for i, txt in enumerate([f'F{i+1}' for i in range(len(corpus))]):
    plt.annotate(txt, (coordenadas_2d[i, 0], coordenadas_2d[i, 1]), fontsize=12, ha='center', va='center')

plt.title('Visualización de Clusters de Frases (K-Means sobre TF-IDF)', fontsize=16)
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.legend(handles=scatter.legend_elements()[0], labels=[f'Cluster {i}' for i in range(num_clusters)], title="Clusters")
plt.grid(True)
plt.show()

print("\n--- FIN DEL EJERCICIO 5 ---")
print("Observación: Mira el gráfico. ¿Las frases que expresan sentimientos similares cayeron en el mismo cluster?")
print("Este es el poder del aprendizaje no supervisado: encontrar patrones (como el sentimiento) sin que se lo hayamos dicho explícitamente.")
