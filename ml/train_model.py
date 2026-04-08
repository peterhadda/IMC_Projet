from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

try:
    from evaluate_model import evaluate_model, save_evaluation_report
    from preprocess import (
        build_preprocessing_pipeline,
        categorical_features,
        feature_columns,
        numeric_features,
        run_preprocessing,
        target_column,
    )
    from save_model import save_feature_config, save_trained_model
except ModuleNotFoundError:
    from ml.evaluate_model import evaluate_model, save_evaluation_report
    from ml.preprocess import (
        build_preprocessing_pipeline,
        categorical_features,
        feature_columns,
        numeric_features,
        run_preprocessing,
        target_column,
    )
    from ml.save_model import save_feature_config, save_trained_model


BASE_DIR = Path(__file__).resolve().parent.parent
best_model_output_path = BASE_DIR / "models" / "best_model.pkl"
feature_config_output_path = BASE_DIR / "models" / "feature_config.json"


def _validate_training_data(X_train, y_train):
    if X_train is None or y_train is None:
        raise ValueError("X_train et y_train ne doivent pas etre None.")
    if len(X_train) != len(y_train):
        raise ValueError("X_train et y_train doivent avoir le meme nombre de lignes.")
    if len(X_train) == 0:
        raise ValueError("Le jeu d'entrainement est vide.")


def _build_training_pipeline(classifier):
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessing_pipeline()),
            ("classifier", classifier),
        ]
    )


def _build_training_result(model_name, model, evaluation_report, extra_data=None):
    result = {
        "model_name": model_name,
        "model_object": model,
        "accuracy": evaluation_report["accuracy"],
        "precision": evaluation_report["precision"],
        "recall": evaluation_report["recall"],
        "f1_score": evaluation_report["f1_score"],
        "main_score": evaluation_report["f1_score"],
        "evaluation_report": evaluation_report,
    }

    if extra_data:
        result.update(extra_data)

    return result


def train_logistic_regression(X_train, y_train, X_test=None, y_test=None):
    _validate_training_data(X_train, y_train)

    trained_model = _build_training_pipeline(
        LogisticRegression(max_iter=1000, random_state=42)
    )
    trained_model.fit(X_train, y_train)

    evaluation_X = X_test if X_test is not None else X_train
    evaluation_y = y_test if y_test is not None else y_train
    evaluation_report = evaluate_model(
        trained_model,
        evaluation_X,
        evaluation_y,
        "Logistic Regression",
    )

    return _build_training_result(
        "Logistic Regression",
        trained_model,
        evaluation_report,
        extra_data={
            "parameters": {
                "max_iter": 1000,
                "random_state": 42,
            }
        },
    )


def train_decision_tree(X_train, y_train, X_test=None, y_test=None):
    _validate_training_data(X_train, y_train)

    classifier = DecisionTreeClassifier(
        random_state=42,
        max_depth=5,
        min_samples_split=2,
        min_samples_leaf=1,
    )
    trained_model = _build_training_pipeline(classifier)
    trained_model.fit(X_train, y_train)

    evaluation_X = X_test if X_test is not None else X_train
    evaluation_y = y_test if y_test is not None else y_train
    evaluation_report = evaluate_model(
        trained_model,
        evaluation_X,
        evaluation_y,
        "Decision Tree",
    )

    return _build_training_result(
        "Decision Tree",
        trained_model,
        evaluation_report,
        extra_data={
            "depth": classifier.get_depth(),
            "n_nodes": classifier.tree_.node_count,
            "parameters": {
                "random_state": 42,
                "max_depth": 5,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
            },
        },
    )


def train_random_forest(X_train, y_train, X_test=None, y_test=None):
    _validate_training_data(X_train, y_train)

    n_estimators = 100
    random_state = 42
    max_depth = 10
    min_samples_split = 2
    min_samples_leaf = 1

    classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
    )
    trained_model = _build_training_pipeline(classifier)
    trained_model.fit(X_train, y_train)

    evaluation_X = X_test if X_test is not None else X_train
    evaluation_y = y_test if y_test is not None else y_train
    evaluation_report = evaluate_model(
        trained_model,
        evaluation_X,
        evaluation_y,
        "Random Forest",
    )

    return _build_training_result(
        "Random Forest",
        trained_model,
        evaluation_report,
        extra_data={
            "parameters": {
                "n_estimators": n_estimators,
                "random_state": random_state,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "min_samples_leaf": min_samples_leaf,
            }
        },
    )


def compare_models(model_results):
    if not model_results:
        raise ValueError("Aucun modele a comparer.")

    best_model = None
    best_score = float("-inf")
    best_model_name = ""

    for result in model_results:
        model_name = result["model_name"]
        model_object = result["model_object"]
        main_score = result["main_score"]

        if main_score > best_score:
            best_score = main_score
            best_model = model_object
            best_model_name = model_name

    sorted_results = sorted(model_results, key=lambda result: result["main_score"], reverse=True)

    return {
        "best_model": best_model,
        "best_score": best_score,
        "best_model_name": best_model_name,
        "sorted_results": sorted_results,
    }


def train_best_model(X_train, y_train, X_test, y_test, feature_config=None):
    candidate_models = [
        ("Logistic Regression", train_logistic_regression),
        ("Decision Tree", train_decision_tree),
        ("Random Forest", train_random_forest),
    ]

    model_results = []

    for model_name, train_function in candidate_models:
        result = train_function(X_train, y_train, X_test, y_test)
        if result["model_name"] != model_name:
            result["model_name"] = model_name
        model_results.append(result)

    comparison = compare_models(model_results)

    best_model = comparison["best_model"]
    best_score = comparison["best_score"]
    best_model_name = comparison["best_model_name"]
    best_result = comparison["sorted_results"][0]

    saved_model_path = save_trained_model(best_model, best_model_output_path)
    evaluation_report_path = save_evaluation_report(best_result["evaluation_report"])
    feature_config_path = None
    if feature_config:
        feature_config = dict(feature_config)
        feature_config["model_name"] = best_model_name
        feature_config_path = save_feature_config(feature_config, feature_config_output_path)

    return {
        "best_model": best_model,
        "best_score": best_score,
        "best_model_name": best_model_name,
        "model_results": model_results,
        "saved_model_path": saved_model_path,
        "evaluation_report": best_result["evaluation_report"],
        "evaluation_report_path": evaluation_report_path,
        "feature_config_path": feature_config_path,
    }


def main():
    preprocessing_result = run_preprocessing()
    encoded_feature_names = []
    training_result = train_best_model(
        preprocessing_result["X_train"],
        preprocessing_result["y_train"],
        preprocessing_result["X_test"],
        preprocessing_result["y_test"],
    )

    best_pipeline = training_result["best_model"]
    if hasattr(best_pipeline.named_steps["preprocessor"], "get_feature_names_out"):
        encoded_feature_names = list(best_pipeline.named_steps["preprocessor"].get_feature_names_out())

    best_classifier = best_pipeline.named_steps["classifier"]
    label_mapping = {
        label: index
        for index, label in enumerate(best_classifier.classes_)
    }

    feature_config = {
        "feature_order": feature_columns,
        "target_column": target_column,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "encoded_feature_names": encoded_feature_names,
        "label_mapping": label_mapping,
        "model_name": training_result["best_model_name"],
    }
    training_result["feature_config_path"] = save_feature_config(feature_config, feature_config_output_path)

    print(f"Meilleur modele: {training_result['best_model_name']}")
    print(f"Meilleur score (test): {training_result['best_score']:.4f}")
    print(f"Modele sauvegarde dans: {training_result['saved_model_path']}")
    print(f"Rapport d'evaluation: {training_result['evaluation_report_path']}")
    if training_result["feature_config_path"]:
        print(f"Configuration features: {training_result['feature_config_path']}")

    for result in training_result["model_results"]:
        print(
            f"{result['model_name']}: "
            f"accuracy={result['accuracy']:.4f}, "
            f"precision={result['precision']:.4f}, "
            f"recall={result['recall']:.4f}, "
            f"f1={result['f1_score']:.4f}, "
            f"statut={result['evaluation_report']['status']}"
        )


if __name__ == "__main__":
    main()
