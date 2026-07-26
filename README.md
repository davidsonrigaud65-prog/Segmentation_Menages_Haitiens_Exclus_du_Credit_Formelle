# 🏦 Segmentation des ménages haïtiens exclus du crédit formel

**Identification des profils prioritaires pour le ciblage d'une offre de microcrédit**

![Status](https://img.shields.io/badge/status-terminé-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Projet réalisé dans le cadre de la formation **Data Science FRST** (Faculté des Sciences — FDS), financée par la **Banque de la République d'Haïti (BRH)**.

---

## 📌 Contexte

En Haïti, **70 % de la population adulte** est exclue du système financier formel, et seulement **4 %** a accès au crédit formel. Les institutions de microfinance (IMF) manquent d'une cartographie fine des ménages non bancarisés pour cibler efficacement une offre de microcrédit.

**Question de recherche :** peut-on segmenter les ménages haïtiens exclus du crédit formel pour identifier ceux les plus susceptibles d'adopter et de rembourser un microcrédit ?

---

## 🗂️ Données

| Paramètre | Valeur |
|---|---|
| Source | FinScope Consumer Haïti 2018 (BRH / DAI / FinMark Trust) |
| Taille totale | 4 269 individus × 34 variables |
| Population cible (filtre) | 4 016 individus — jamais eu de crédit formel (94,1 %) |
| Variables retenues | 17 (numériques, binaires, ordinales, nominale encodée) |
| Valeurs manquantes | 0 sur les variables de clustering |

---

## 🧪 Méthodologie

```
Standardisation (z-score) → AFDM (12 composantes, 85% variance) → Choix de k → K-means (k=6) → Validation (ARI Bootstrap)
```

**5 algorithmes de clustering comparés** : K-means, CAH (Ward), K-médoïdes (PAM), méthode mixte CAH+K-means, DBSCAN.

**K-means (k=6)** a été retenu comme le plus robuste :

| Méthode | Silhouette | Calinski-Harabasz | Davies-Bouldin | Décision |
|---|---|---|---|---|
| **K-means k=6** | **0,2683** | **638,12** | **1,4631** | ✅ Retenu |
| CAH Ward | 0,2136 | 512,91 | 1,7639 | Validation indépendante |
| K-médoïdes PAM | 0,1421 | 347,43 | 2,0552 | Médoïdes réels |
| DBSCAN | 0,2466 | — | — | 20 clusters (structure globulaire) |

**Robustesse validée par :**
- ARI Bootstrap = **1,000** (std = 0,000, 50 runs) → stabilité parfaite
- ARI sans variable revenu = **0,997** → structure multidimensionnelle confirmée
- 0 % d'individus ambigus (silhouette individuelle)

---

## 📊 Résultats — 6 segments identifiés

| Segment | % population | Revenu médian | Score priorité /100 | Statut |
|---|---|---|---|---|
| Salariés formels | 7,6 % | 11 207 HTG | **80,3** | 🟢 Prioritaire |
| Commerçants informels | 25,5 % | 4 028 HTG | 51,3 | 🟡 Secondaire |
| Prestataires de services | 13,2 % | 5 320 HTG | 45,1 | 🟡 Secondaire |
| Ménages sans revenus | 14,9 % | 746 HTG | 26,4 | 🔴 Non prioritaire |
| Artisans | 10,9 % | 3 391 HTG | 24,2 | 🔴 Non prioritaire |
| Agriculteurs vulnérables | 27,8 % | 1 875 HTG | 12,6 | 🔴 Non prioritaire |

**Score de priorité microcrédit** = Tontine×0,20 + CIN×0,20 + Revenu×0,20 + Exclusion×0,15 + Manque d'argent×0,15 + Téléphone×0,10

---

## 💡 Recommandations produits

| Segment | Produit recommandé | Montant |
|---|---|---|
| Salariés formels | Prêt personnel / professionnel | 15 000 – 50 000 HTG |
| Commerçants informels | Microcrédit groupé (tontines) | 5 000 – 20 000 HTG |
| Prestataires de services | Crédit numérique mobile money | 3 000 – 15 000 HTG |
| Artisans | Crédit équipement | 10 000 – 30 000 HTG |
| Ménages sans revenus / Agriculteurs | Épargne d'abord / Programme BRH | — |

---

## 📁 Structure du dépôt

```
├── data/                  # Données (échantillon — voir note ci-dessous)
├── notebooks/
│   ├── eda.ipynb          # Analyse exploratoire
│   ├── clustering.ipynb   # Comparaison des algorithmes & choix de k
│   └── evaluation.ipynb   # Validation (Silhouette, ARI, Eta²)
├── predict.py             # Pipeline reproductible de segmentation
├── dashboard/              # Dashboard Power BI (.pbix)
├── presentation/            # Slides de présentation (.pptx)
├── requirements.txt         # Dépendances Python
└── README.md
```

> ⚠️ **Note sur les données** : le dossier `data/` contient un échantillon à des fins de démonstration. Le jeu de données complet FinScope Haïti 2018 doit être obtenu auprès de la BRH / FinMark Trust.

---

## ⚙️ Installation et utilisation

```bash
# Cloner le dépôt
git clone https://github.com/VOTRE-USERNAME/nom-du-repo.git
cd nom-du-repo

# Installer les dépendances
pip install -r requirements.txt

# Lancer la segmentation sur de nouvelles données
python predict.py --input data/nouveau_fichier.csv
```

```python
from predict import predire_segments

segments = predire_segments(mon_dataframe)
```

Pipeline testé avec un **accord de 100 %** sur les données de validation.

---

## ⚖️ Éthique et limites

- Aucune donnée individuelle réelle n'est publiée dans ce dépôt.
- La segmentation est conçue comme une **aide à la décision**, non comme un système d'exclusion automatique de crédit.
- Biais de genre documenté (participation aux tontines : 45,6 % femmes vs 35,3 % hommes).
- Limites principales : sous-représentation rurale dans l'échantillon (29,3 % vs ~45 % réel), données datant de 2018, deux variables non discriminantes (Age, Crédit_Informel) à retirer en v2.
- Une validation externe est recommandée avant tout déploiement réel.

---

## 👥 Équipe

- **Davidson RIGAUD**
- **Abdarare HERARD**
- **Roodson FRANCOIS**

**Encadrant :** M. Evens TOUSSAINT
**Groupe 5 — FDS/FRST — Capstone 2025-2026**

*Formation financée par la Banque de la République d'Haïti (BRH).*

---

## 📄 Licence

Ce projet est distribué sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus de détails.
