# 💳 Catching Fraudsters: Credit Card Fraud Detection

> **Can a model reliably flag fraudulent transactions in a dataset where fraud is rarer than 1 in 500?**  
> Logistic regression and random forest classification in both R and Python on 284,807 transactions.

![Precision-Recall Curve](figures/py_02_precision_recall.png)

---

## 📋 Table of Contents
- [Problem](#problem)
- [Data](#data)
- [Methods](#methods)
- [Key Results](#key-results)
- [Business Insights](#business-insights)
- [How to Reproduce](#how-to-reproduce)
- [What I'd Do Next](#what-id-do-next)

---

## Problem

Credit card fraud costs the global economy tens of billions of dollars annually. The core challenge is **extreme class imbalance** — fraud is rare, so a model that predicts "not fraud" for every transaction achieves 99.8% accuracy but catches zero frauds.

This project builds and compares two classification models to:

1. Detect fraudulent transactions (binary outcome: Fraud / Not Fraud)
2. Handle severe class imbalance using SMOTE and class weighting
3. Evaluate using precision-recall and AUC-PR (not just accuracy)
4. Identify which transaction features most strongly predict fraud

The same analysis is implemented in **both R and Python** — comparing model performance across both.

---

## Data

| Property | Detail |
|---|---|
| **Source** | [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| **Size** | 284,807 transactions × 31 columns |
| **Target** | `Class` — Fraud (492, 0.17%) / Not Fraud (284,315, 99.83%) |
| **Time period** | Two days of European cardholder transactions (September 2013) |
| **License** | DbCL v1.0 via Kaggle |

### Key Variables

| Variable | Type | Description |
|---|---|---|
| `V1`–`V28` | numeric | PCA-transformed features (original features confidential) |
| `Time` | numeric | Seconds elapsed since first transaction |
| `Amount` | numeric | Transaction amount (€) |
| `Class` | **target** | 1 = Fraud, 0 = Not Fraud |

> **Note:** Due to confidentiality, the original feature names are unavailable. All features except `Time` and `Amount` are PCA components.

---

## Methods

### R (`R/fraud_detection.R`)
| Step | Function | Package |
|---|---|---|
| EDA | `ggplot2` density + boxplot | ggplot2 |
| Train/test split | `createDataPartition()` | caret |
| Class imbalance | `SMOTE()` | DMwR2 |
| Logistic regression | `glm(family = binomial)` | base R |
| Random forest | `randomForest()` | randomForest |
| Feature importance | `varImpPlot()` | randomForest |
| Confusion matrix | `confusionMatrix()` | caret |
| Precision-Recall | `pr.curve()` | PRROC |
| ROC / AUC | `roc()`, `auc()` | pROC |
| Hypothesis test | `Anova(type = "II")` | car |

### Python (`Python/fraud_detection.py`)
| Step | Function | Package |
|---|---|---|
| EDA | `boxplot`, `hist`, `heatmap` | matplotlib / seaborn |
| Preprocessing | `StandardScaler()` | scikit-learn |
| Class imbalance | `SMOTE()` | imbalanced-learn |
| Logistic regression | `LogisticRegression(class_weight="balanced")` | scikit-learn |
| Random forest | `RandomForestClassifier(class_weight="balanced")` | scikit-learn |
| Cross-validation | `StratifiedKFold` + `cross_val_score` | scikit-learn |
| Precision-Recall curve | `PrecisionRecallDisplay` | scikit-learn |
| ROC curve | `RocCurveDisplay` | scikit-learn |
| Feature importance | `feature_importances_` | scikit-learn |

---

## Key Results

### Model Performance

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| **ROC-AUC** | ~0.97 | ~0.99 |
| **AUC-PR** | ~0.75 | ~0.87 |
| Precision (Fraud) | ~0.87 | ~0.95 |
| Recall (Fraud) | ~0.63 | ~0.82 |
| F1-Score (Fraud) | ~0.73 | ~0.88 |

> ROC-AUC overstates performance under class imbalance. **AUC-PR is the primary metric here** — it penalises the model for missing actual frauds and for false alarms.

> Both R and Python implementations converge to the same performance, validating the analysis.

### Top Fraud Predictors (Random Forest Feature Importance)

| Rank | Feature | Interpretation |
|---|---|---|
| 1 | `V14` | Strongest negative signal for fraud |
| 2 | `V4` | Positive association with fraud |
| 3 | `V12` | Strong fraud indicator |
| 4 | `V10` | Negative fraud signal |
| 5 | `Amount` | Higher amounts slightly associated with fraud |

### 6-Step Hypothesis Test: Amount Effect on Fraud
1. **α = 0.05**
2. **H₀:** β_Amount = 0 (transaction amount has no effect on fraud probability)
3. **Decision rule:** Reject H₀ if p-value ≤ α
4. **Test statistic:** χ² (from Type II likelihood-ratio test on logistic model)
5. **p-value < 0.001**
6. **Conclusion:** Reject H₀ — transaction amount significantly predicts fraud probability

---

## Business Insights

| Finding | Implication |
|---|---|
| Recall (fraud caught) matters more than precision | Missing a fraud costs more than flagging a legitimate transaction for review |
| Random forest outperforms logistic regression | Non-linear feature interactions exist in the PCA components |
| `Amount` is a weak predictor on its own | Fraudsters operate across all transaction sizes — amount alone is insufficient |
| SMOTE meaningfully improves recall | Without oversampling, models learn to ignore the minority class |
| AUC-PR drops significantly vs ROC-AUC | Always report both metrics; ROC-AUC flatters models on imbalanced data |

---

## How to Reproduce

### R
```r
# Install once
install.packages(c("tidyverse", "caret", "randomForest", "pROC", "PRROC", "car", "DMwR2"))

# Run
source("R/fraud_detection.R")
```

### Python
```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn

python Python/fraud_detection.py
```

---

## What I'd Do Next
- Try **XGBoost or LightGBM** — gradient boosting typically dominates on tabular fraud data
- Apply **threshold tuning** — choose the classification cutoff that minimises business cost, not just F1
- Add **SHAP values** for explainability — important for real-world fraud systems that must justify decisions
- Explore **isolation forest or autoencoders** as unsupervised anomaly detection baselines
- Test on a **time-based train/test split** (train on day 1, test on day 2) to simulate real deployment

---

*Data: ULB Machine Learning Group — Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson, Gianluca Bontempi (2015).*
