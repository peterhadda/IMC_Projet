from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score


def train_logistic_regression(X_train, y_train):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

def train_decision_tree(X_train, y_train):

    # =========================
    # 1. Vérifications
    # =========================
    if X_train is None or y_train is None:
        return None

    if len(X_train) != len(y_train):
        raise ValueError("X_train and y_train must have the same length")

    # =========================
    # 2. Initialisation
    # =========================
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5,
        min_samples_split=2,
        min_samples_leaf=1
    )

    # =========================
    # 3. Entraînement
    # =========================
    model.fit(X_train, y_train)

    # =========================
    # 4. Prédictions
    # =========================
    y_pred = model.predict(X_train)

    # =========================
    # 5. Métriques
    # =========================
    accuracy = accuracy_score(y_train, y_pred)
    precision = precision_score(y_train, y_pred, average="weighted")
    recall = recall_score(y_train, y_pred, average="weighted")
    f1_value = f1_score(y_train, y_pred, average="weighted")

    main_score = f1_value

    # =========================
    # 6. Infos arbre
    # =========================
    profondeur_arbre = model.get_depth()
    nombre_noeuds = model.tree_.node_count

    # =========================
    # 7. Résultat structuré
    # =========================
    resultat = {
        "model_name": "Decision Tree",
        "model_object": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_value,
        "main_score": main_score,
        "depth": profondeur_arbre,
        "n_nodes": nombre_noeuds
    }

    return resultat
