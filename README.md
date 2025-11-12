# Annotation et Classification du Pronom "on"

## 🎯 Objectif

Ce projet vise à :
- Annoter manuellement les occurrences du pronom **"on"** dans un corpus d'apprenants du français.
- Développer un **classifieur automatique** capable de distinguer ses différents usages :
  - **nous** (inclusif),
  - **indéfini** (valeur générique),
  
L’étude repose sur le corpus **TCFLE-8** (Test de Connaissance du Français Langue Étrangère – 2023).


## 🗃️ Données

**⚠️ Les données ne sont pas publiques.**

Le corpus contient :
- Des textes d'apprenants de différentes langues (japonais, chinois, arabe, portugais...)
- Des niveaux de langue CECRL (A1 à C2)
- Des métadonnées sur chaque participant (langue maternelle...)


## 📝 Annotation

- Annotation manuelle
- Calculs de **kappa de Cohen** pour l’évaluation de l’accord inter-annotateurs.


## 🧠 Classifieur Automatique

1. **Nettoyage du corpus** : extraction des lignes contenant "on", suppression des balises inutiles.
2. **Extraction de contextes** :
   - 10 mots à gauche et à droite de chaque "on"
   - Arrêt au niveau de la ponctuation
3. **Vectorisation** avec `TfidfVectorizer`
4. **Classification** avec `LogisticRegression` (Sklearn)
5. **Évaluation** :
   - Méthode `split` (80/20)
   - Méthode `cross-validation` (10 folds)

### 📊 Résultats :
- **Accuracy moyenne** : ~85%
- **Kappa de Cohen** : ~0.9

## 👥 Contributeurs

- [Keren DAGUE](https://github.com/KerenDague)
- [Maiwenn PLEVENAGE](https://github.com/00parts)
- [Juliette HENRY](https://github.com/juliettehnr)
- Pauline Fillols (M1 FLDL)
