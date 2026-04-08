import json
import pickle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
default_model_path = BASE_DIR / "models" / "best_model.pkl"
default_feature_config_path = BASE_DIR / "models" / "feature_config.json"


def save_trained_model(model, output_path=default_model_path):
    if model is None:
        raise ValueError("Le modele a sauvegarder est absent.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("wb") as model_file:
        pickle.dump(model, model_file)

    return str(output_path)


def load_trained_model(model_path=default_model_path):
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Modele introuvable: {model_path}")

    with model_path.open("rb") as model_file:
        return pickle.load(model_file)


def save_feature_config(config_data, output_path=default_feature_config_path):
    if not config_data:
        raise ValueError("Les metadonnees du modele sont absentes.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    serializable_config = {
        "feature_order": list(config_data.get("feature_order", [])),
        "label_mapping": dict(config_data.get("label_mapping", {})),
        "target_column": config_data.get("target_column"),
        "numeric_features": list(config_data.get("numeric_features", [])),
        "categorical_features": list(config_data.get("categorical_features", [])),
        "encoded_feature_names": list(config_data.get("encoded_feature_names", [])),
        "model_name": config_data.get("model_name"),
    }

    with output_path.open("w", encoding="utf-8") as config_file:
        json.dump(serializable_config, config_file, indent=2, ensure_ascii=False)

    return str(output_path)


def load_feature_config(config_path=default_feature_config_path):
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration features introuvable: {config_path}")

    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
