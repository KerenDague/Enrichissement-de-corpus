"""
Extraction du contexte autour du pronom 'on' dans un corpus annoté.

Ce script lit un fichier CSV contenant des phrases où les occurrences du mot "on" sont balisées par <i>on</i> (usage indéfini) ou <n>on</n> (usage inclusif "nous").
Il extrait pour chaque "on" :
- Le contexte gauche (quelques mots avant),
- Le contexte droit (quelques mots après),
- Le label associé ("indéfini" ou "nous").

Le résultat est une liste de dictionnaires, chacun contenant :
- 'contexte_gauche' : mots précédant "on",
- 'on' : le mot "on",
- 'contexte_droit' : mots suivant "on",
- 'label' : type d'usage de "on".

"""
import pandas as pd
import spacy
import json

nlp = spacy.load("fr_core_news_md")

df = pd.read_csv("B2.csv") 

# Fonction pour récupérer un contexte limité par ponctuation ou nombre de mots
def recuperer_contexte(tokens, start_idx, direction, max_mots=10):
    contexte = []
    if direction == "gauche":
        indices = range(start_idx - 1, -1, -1)  # Partir en arrière
    else:
        indices = range(start_idx + 1, len(tokens))  # Aller en avant
    
    for idx in indices:
        if tokens[idx].text in [".", "?", "!", ";"]:
            break  # On arrête si ponctuation de fin de phrase
        contexte.append(tokens[idx].text)
        if len(contexte) >= max_mots:
            break
    
    if direction == "gauche":
        contexte.reverse()  # Pour garder l'ordre naturel
    return " ".join(contexte)

# Fonction principale d'extraction
def extraire_contextes_et_label(texte):
    resultats = []
    if not isinstance(texte, str):
        return resultats

    texte_modifie = texte.replace('<i>on</i>', ' ON_INDEFINI ').replace('<n>on</n>', ' ON_NOUS ')
    doc = nlp(texte_modifie)

    for i, token in enumerate(doc):
        if token.text in ['ON_INDEFINI', 'ON_NOUS']:
            label = 'indéfini' if token.text == 'ON_INDEFINI' else 'nous'
            contexte_gauche = recuperer_contexte(doc, i, direction="gauche", max_mots=10)
            contexte_droit = recuperer_contexte(doc, i, direction="droite", max_mots=10)
            resultat = {
                "contexte_gauche": contexte_gauche,
                "contexte_droit": contexte_droit,
                "label": label
            }
            resultats.append(resultat)
    return resultats

# Appliquer au corpus
dictionnaires = []
for texte in df['Réponse au test']: 
    dictionnaires.extend(extraire_contextes_et_label(texte))

# Sauvegarder le résultat
with open("contextes_on.json", "w", encoding="utf-8") as f:
    json.dump(dictionnaires, f, ensure_ascii=False, indent=2)
print("Extraction terminée, résultat sauvegardé dans contextes_on.json")
