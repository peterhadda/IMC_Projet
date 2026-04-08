import json
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


BASE_DIR = Path(__file__).resolve().parent.parent
evaluation_report_output_path = BASE_DIR / "models" / "evaluation_report.json"
minimum_accepted_f1_score = 0.60


def _validate_evaluation_inputs(model, X_test, y_test):
    if model is None:
        raise ValueError("Le modele est absent.")
    if X_test is None or y_test is None:
        raise ValueError("Les donnees de test sont absentes.")
    if len(X_test) != len(y_test):
        raise ValueError("X_test et y_test doivent avoir la meme taille.")
    if len(X_test) == 0:
        raise ValueError("Le jeu de test est vide.")


def _predict(model, X_test, y_test):
    _validate_evaluation_inputs(model, X_test, y_test)
    return model.predict(X_test)


def evaluate_accuracy(model, X_test, y_test):
    predictions = _predict(model, X_test, y_test)
    return accuracy_score(y_test, predictions)


def evaluate_precision(model, X_test, y_test):
    predictions = _predict(model, X_test, y_test)
    return precision_score(y_test, predictions, average="weighted", zero_division=0)


def evaluate_recall(model, X_test, y_test):
    predictions = _predict(model, X_test, y_test)
    return recall_score(y_test, predictions, average="weighted", zero_division=0)


def evaluate_f1_score(model, X_test, y_test):
    predictions = _predict(model, X_test, y_test)
    return f1_score(y_test, predictions, average="weighted", zero_division=0)


def build_evaluation_report(metrics_data):
    if not metrics_data:
        raise ValueError("Les metriques sont absentes.")

    accuracy = metrics_data["accuracy"]
    precision = metrics_data["precision"]
    recall = metrics_data["recall"]
    f1_value = metrics_data["f1_score"]
    model_name = metrics_data.get("model_name", "Modele inconnu")

    is_validated = f1_value >= minimum_accepted_f1_score
    validation_status = "Modele valide" if is_validated else "Modele non valide"

    return {
        "model_name": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_value,
        "status": validation_status,
        "is_validated": is_validated,
        "minimum_accepted_f1_score": minimum_accepted_f1_score,
        "gui_decision": "autoriser" if is_validated else "interdire",
        "message": "Le modele peut etre utilise uniquement s'il a ete valide.",
    }


def evaluate_model(model, X_test, y_test, model_name):
    metrics_data = {
        "model_name": model_name,
        "accuracy": evaluate_accuracy(model, X_test, y_test),
        "precision": evaluate_precision(model, X_test, y_test),
        "recall": evaluate_recall(model, X_test, y_test),
        "f1_score": evaluate_f1_score(model, X_test, y_test),
    }
    return build_evaluation_report(metrics_data)


def save_evaluation_report(evaluation_report, output_path=evaluation_report_output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as report_file:
        json.dump(evaluation_report, report_file, indent=2, ensure_ascii=False)
    return str(output_path)
