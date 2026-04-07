import json
from pathlib import Path


class RecommendationService:
    def __init__(self, json_path=None):
        default_path = Path(__file__).resolve().parent.parent / "data" / "recommandations.json"
        self.json_path = Path(json_path) if json_path else default_path
        self.category_advice_map = {}
        self.risk_advice_map = {}
        self._load_recommendations()

    def _load_recommendations(self):
        with self.json_path.open("r", encoding="utf-8") as json_file:
            payload = json.load(json_file)

        for entry in payload.get("recommandations", []):
            category = entry.get("classification")
            risk = entry.get("risque")
            conseils = entry.get("conseils", [])
            if category:
                self.category_advice_map[category] = conseils
            if risk and risk not in self.risk_advice_map:
                self.risk_advice_map[risk] = self._build_risk_message(risk)

    def _build_risk_message(self, risk_level):
        messages = {
            "Moindre": "Le risque reste faible si vous gardez une bonne hygiene de vie.",
            "Accru": "Une attention supplementaire est conseillee pour eviter une aggravation.",
            "Eleve": "Un suivi regulier est recommande pour reduire les complications.",
            "Tres eleve": "Un accompagnement medical est fortement recommande.",
            "Extremement eleve": "Une prise en charge medicale rapide est recommandee.",
        }
        return messages.get(risk_level, "Surveillez regulierement votre etat de sante.")

    def get_recommendation_by_category(self, bmi_category):
        return self.category_advice_map.get(
            bmi_category,
            ["Aucune recommandation disponible pour cette categorie."],
        )

    def get_recommendation_by_risk(self, risk_level):
        return self.risk_advice_map.get(
            risk_level,
            "Surveillez regulierement votre etat de sante.",
        )

    def build_recommendation_text(self, user_profile, bmi_result):
        recommendation_lines = list(self.get_recommendation_by_category(bmi_result["bmi_category"]))
        recommendation_lines.append(self.get_recommendation_by_risk(bmi_result["risk_level"]))

        if user_profile.get("activity_level") == "Faible":
            recommendation_lines.append("Essayez d'ajouter un peu d'activite physique chaque semaine.")
        if user_profile.get("age", 0) >= 50:
            recommendation_lines.append("Un bilan regulier peut etre utile compte tenu de l'age.")

        return "\n".join("- " + line for line in recommendation_lines)
