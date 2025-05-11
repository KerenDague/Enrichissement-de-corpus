"""
Script de classification du pronom 'on' en français selon son contexte.

Le script extrait le contexte autour de 'on' dans une phrase, vectorise ce contexte avec TF-IDF,
et entraîne une régression logistique pour prédire l'interprétation du pronom.

"""

#import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import json
from sklearn.metrics import accuracy_score


# === Entraînement ===


with open('contextes_on.json') as corpus_json :
    data = json.load(corpus_json)

corpus = []
labels = []
for texte_dict in data :
    texte = texte_dict['contexte_gauche'] + texte_dict['contexte_droit']
    corpus.append(texte)
    label = texte_dict['label']
    labels.append(label)
corpus_context = corpus

# === Split du corpus en corpus test et train, 30% de test et 70% de train ===
corpus_train, corpus_test, labels_train, labels_test = train_test_split(corpus_context, labels, test_size=0.30)

# === Entraînement du modèle sur le corpus train ===
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
X = vectorizer.fit_transform(corpus_train)
model = LogisticRegression()
model.fit(X, labels_train)


# === Prédiction ===
def classifie_on(corpus_test):
    predictions = []
    for i in range(len(corpus_test)) :
        phrase = corpus_test[i]
        vecteur = vectorizer.transform([phrase])
        prediction = model.predict(vecteur)[0]
        predictions.append(prediction)
        print(f"\nPhrase : {phrase}")
        print(f"→ Interprétation de 'on' : **{prediction}**")
        print(f"Réelle valeur du on : {labels_test[i]}")
        
    score_pourcentage = accuracy_score(labels_test, predictions)
    score_count = accuracy_score(labels_test, predictions, normalize=False)
    print(f"\n{score_pourcentage * 100}% de bonnes prédictions, soit {score_count} bonnes prédictions sur {len(predictions)}")

# === Exemple ===
if __name__ == "__main__":
    classifie_on(corpus_test)



