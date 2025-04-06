import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Initialisation
nlp = spacy.load("fr_core_news_md")

# Fonction d’extraction de contexte
def extract_context(text):
    doc = nlp(text)
    for i, token in enumerate(doc):
        if token.text.lower() == "on":
            left = doc[max(i-3, 0):i]
            right = doc[i+1:i+4]
            return " ".join([tok.text for tok in left]) + " on " + " ".join([tok.text for tok in right])
    return text

# === Entraînement ===
corpus = [
    "On va au cinéma ce soir.",
    "On a toujours dit que c'était vrai.",
    "On mange ensemble demain ?",
    "On dit qu’il va pleuvoir demain.",
    "On a gagné le match !",
    "On parle souvent de ce problème.",
]

labels = ["nous", "indéfini", "nous", "indéfini", "nous", "indéfini"]

corpus_context = [extract_context(text) for text in corpus]
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
X = vectorizer.fit_transform(corpus_context)

model = LogisticRegression()
model.fit(X, labels)

# === Prédiction ===
def classifie_on(phrase):
    contexte = extract_context(phrase)
    vecteur = vectorizer.transform([contexte])
    prediction = model.predict(vecteur)[0]
    print(f"\nPhrase : {phrase}")
    print(f"Contexte extrait : {contexte}")
    print(f"→ Interprétation de 'on' : **{prediction}**")

# === Exemple ===
if __name__ == "__main__":
    classifie_on("On doit terminer ce projet à temps.")
    classifie_on("On raconte que cette histoire est vraie.")
