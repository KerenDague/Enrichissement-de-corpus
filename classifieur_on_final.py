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
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
import argparse
from sklearn.metrics import confusion_matrix

# === Entraînement ===

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=1000)


def initialiser():
    with open('contextes_on.json') as corpus_json :
        data = json.load(corpus_json)

    global corpus 
    corpus = []
    global labels
    labels = []
    for texte_dict in data :
        texte = texte_dict['contexte_gauche'] + texte_dict['contexte_droit']
        corpus.append(texte)
        label = texte_dict['label']
        labels.append(label)

    
def split() :
# === Split du corpus en corpus test et train, 30% de test et 70% de train ===

    corpus_train, corpus_test, labels_train, labels_test = train_test_split(corpus, labels, test_size=0.20)

    X_train = vectorizer.fit_transform(corpus_train)
    X_test = vectorizer.transform(corpus_test)
    model = LogisticRegression()
    model = model.fit(X_train, labels_train)

    predictions = []
    for i in range(len(corpus_test)) :
        phrase = corpus_test[i]
        vecteur = X_test[i]
        prediction = model.predict(vecteur)[0]
        predictions.append(prediction)
        print(f"\nPhrase : {phrase}")
        print(f"→ Interprétation de 'on' : **{prediction}**")
        print(f"Réelle valeur du on : {labels_test[i]}")

    score_pourcentage = accuracy_score(labels_test, predictions)
    score_count = accuracy_score(labels_test, predictions, normalize=False)
    cohen = cohen_kappa_score(labels_test, predictions)
    print(f"\n{score_pourcentage * 100}% de bonnes prédictions, soit {score_count} bonnes prédictions sur {len(predictions)}")
    print(f"Kappa de Cohen : {cohen}")

    confusionmatrix = confusion_matrix(labels_test, predictions, labels=["nous", "indéfini"])
    print('\n', confusionmatrix)
 
    return model
    

# === Entraînement du modèle sur le corpus train ===

  

def cross() :

    corpus_train, corpus_test, labels_train, labels_test = train_test_split(corpus, labels, test_size=0.10)


    X_train = vectorizer.fit_transform(corpus_train)
    X_test = vectorizer.transform(corpus_test)
    model = LogisticRegression()
    model = model.fit(X_train, labels_train)

    cv_results = cross_validate(model, X_train, labels_train, cv=10, return_estimator=True)

    results = cv_results['test_score']
    print("\nScores de la cross validation train :", results)
    results_mean = cv_results['test_score'].mean()
    print("Score moyen de la cross validation train:", results_mean)

    test_score = []
    for i in range(len(cv_results['estimator'])):
        test_score.append(cv_results['estimator'][i].score(X_test, labels_test))
    print("Score moyen sur le corpus test :", sum(test_score) / len(test_score))
    return cv_results


# === Prédiction ===
def classifie_on(phrase, models):

    print(f"\nPhrase : {phrase}")
    vecteur = vectorizer.transform([phrase])

    if isinstance(models, LogisticRegression) :
        prediction = model.predict(vecteur)[0]
        print(f"→ Interprétation de 'on' : **{prediction}**")


    elif isinstance(models, dict) :
        for i in range(len(models['estimator'])):
            prediction = models['estimator'][i].predict(vecteur)[0]
            print(f"→ Interprétation de 'on' : **{prediction}**")

   
    

    

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("methode", choices=["split", "cross"], help="choisir si on veut utiliser la cross-validation ou un seul split")
    my_parser.add_argument("phrase", help="phrase contenant un 'on' à classifier", nargs="?")
    my_args = my_parser.parse_args()
    initialiser()
    if my_args.methode == "split" :
        model = split()
        if my_args.phrase : 
            classifie_on(my_args.phrase, model)
        

    elif my_args.methode == "cross":
        
        model = cross()
        if my_args.phrase :
            classifie_on(my_args.phrase, model)

    



'''scores = cross_val_score(model, X, labels_train, cv=10)
    print('Scores de validation croisée : ', scores)
    mean_score = scores.mean()
    print('Score moyen de validation croisée : ', mean_score)'''