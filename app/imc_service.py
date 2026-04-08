class IMCService:
    def calculate_bmi(self, weight, height):
        bmi_value = weight / (height ** 2)
        return bmi_value

    def classify_bmi(self, bmi_value):
        if bmi_value < 18.5:
            return "Poids insuffisant"
        if bmi_value < 25:
            return "Poids normal"
        if bmi_value < 30:
            return "Exces de poids"
        if bmi_value < 35:
            return "Obesite classe I"
        if bmi_value < 40:
            return "Obesite classe II"
        return "Obesite classe III"

    def determine_risk_level(self, bmi_category):
        risk_by_category = {
            "Poids insuffisant": "Accru",
            "Poids normal": "Moindre",
            "Exces de poids": "Accru",
            "Obesite classe I": "Eleve",
            "Obesite classe II": "Tres eleve",
            "Obesite classe III": "Extremement eleve",
        }
        return risk_by_category.get(bmi_category, "Inconnu")

    def build_bmi_result(self, weight, height, bmi_value=None, bmi_category=None, risk_level=None):
        bmi_value = bmi_value if bmi_value is not None else self.calculate_bmi(weight, height)
        bmi_category = bmi_category if bmi_category is not None else self.classify_bmi(bmi_value)
        risk_level = risk_level if risk_level is not None else self.determine_risk_level(bmi_category)

        return {
            "weight": weight,
            "height": height,
            "bmi_value": round(bmi_value, 2),
            "bmi_category": bmi_category,
            "risk_level": risk_level,
            "risk_level_rule": risk_level,
        }
