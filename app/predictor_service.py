import json
from pathlib import Path

import pandas as pd

from ml.save_model import load_feature_config, load_trained_model


class PredictorService:
    def __init__(self, model_path, feature_config_path, evaluation_report_path=None):
        self.model_path = Path(model_path)
        self.feature_config_path = Path(feature_config_path)
        self.evaluation_report_path = Path(evaluation_report_path) if evaluation_report_path else None
        self.model = None
        self.feature_config = None
        self.evaluation_report = None
        self.model_available = False
        self.load_prediction_model()

    def load_prediction_model(self):
        if not self.model_path.exists() or not self.feature_config_path.exists():
            self.model = None
            self.feature_config = None
            self.model_available = False
            return None

        self.model = load_trained_model(self.model_path)
        self.feature_config = load_feature_config(self.feature_config_path)
        self.evaluation_report = self._load_evaluation_report()
        self.model_available = True
        return self.model

    def _load_evaluation_report(self):
        if not self.evaluation_report_path or not self.evaluation_report_path.exists():
            return None

        with self.evaluation_report_path.open("r", encoding="utf-8") as report_file:
            return json.load(report_file)

    def _ensure_model_ready(self):
        if not self.model_available or self.model is None or self.feature_config is None:
            raise RuntimeError("Le modele ML n'est pas disponible.")

    def _normalize_gender(self, gender_value):
        mapping = {
            "Homme": "male",
            "Femme": "female",
            "Autre": "other",
            "male": "male",
            "female": "female",
            "other": "other",
        }
        return mapping.get(gender_value, "other")

    def _normalize_activity(self, activity_value):
        mapping = {
            "Faible": "low",
            "Moderee": "medium",
            "Elevee": "high",
            "low": "low",
            "medium": "medium",
            "high": "high",
        }
        return mapping.get(activity_value, "medium")

    def _format_risk_label(self, label):
        display_mapping = {
            "low_risk": "Risque faible",
            "moderate_risk": "Risque modere",
            "high_risk": "Risque eleve",
        }
        return display_mapping.get(label, label)

    def build_model_input(self, user_data):
        if not user_data:
            raise ValueError("Les donnees utilisateur sont absentes.")

        weight = float(user_data["weight"])
        height = float(user_data["height"])
        age = int(user_data["age"])
        bmi_value = round(weight / (height ** 2), 2)

        input_vector = {
            "age": age,
            "gender": self._normalize_gender(user_data["gender"]),
            "height": height,
            "weight": weight,
            "bmi": bmi_value,
            "activity_level": self._normalize_activity(user_data["activity_level"]),
        }

        ordered_features = self.feature_config.get("feature_order", list(input_vector.keys()))
        return pd.DataFrame([[input_vector[feature] for feature in ordered_features]], columns=ordered_features)

    def predict_risk(self, user_data):
        self._ensure_model_ready()
        input_vector = self.build_model_input(user_data)
        predicted_label = self.model.predict(input_vector)[0]
        prediction_probability = self.predict_probability(user_data)
        is_validated = True
        validation_status = "Modele valide"
        warning_message = None

        if self.evaluation_report:
            is_validated = self.evaluation_report.get("is_validated", False)
            validation_status = self.evaluation_report.get("status", validation_status)
            if not is_validated:
                warning_message = "Modele non valide académiquement. Prediction affichee a titre indicatif."

        return {
            "predicted_risk": predicted_label,
            "confidence_score": prediction_probability,
            "model_name": self.feature_config.get("model_name", type(self.model).__name__),
            "model_version": self.feature_config.get("model_name", type(self.model).__name__),
            "is_validated": is_validated,
            "validation_status": validation_status,
            "warning_message": warning_message,
        }

    def predict_probability(self, user_data):
        self._ensure_model_ready()
        input_vector = self.build_model_input(user_data)
        if not hasattr(self.model, "predict_proba"):
            return None

        probabilities = self.model.predict_proba(input_vector)[0]
        return round(float(max(probabilities)), 4)

    def format_prediction_output(self, prediction_result):
        if not prediction_result:
            return "Aucune prediction disponible."

        predicted_risk = self._format_risk_label(prediction_result["predicted_risk"])
        confidence_score = prediction_result.get("confidence_score")
        model_name = prediction_result.get("model_name", "Modele inconnu")
        validation_status = prediction_result.get("validation_status", "Statut inconnu")
        warning_message = prediction_result.get("warning_message")

        confidence_text = "N/A" if confidence_score is None else f"{confidence_score:.2%}"
        output = (
            f"Prediction ML: {predicted_risk}\n"
            f"Confiance: {confidence_text}\n"
            f"Modele: {model_name}\n"
            f"Statut: {validation_status}"
        )
        if warning_message:
            output += f"\nAvertissement: {warning_message}"
        return output
