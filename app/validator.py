class UserInputValidator:
    def __init__(self):
        self.min_weight = 20.0
        self.max_weight = 300.0
        self.min_height = 0.8
        self.max_height = 2.5
        self.min_age = 1
        self.max_age = 120
        self.allowed_genders = {"Homme", "Femme", "Autre"}
        self.allowed_activity_levels = {"Faible", "Moderee", "Elevee"}

    def validate_weight(self, weight_value):
        weight = self._to_float(weight_value, "Le poids doit etre un nombre valide.")
        if not self.min_weight <= weight <= self.max_weight:
            raise ValueError(f"Le poids doit etre compris entre {self.min_weight} et {self.max_weight} kg.")
        return weight

    def validate_height(self, height_value):
        height = self._to_float(height_value, "La taille doit etre un nombre valide.")
        if not self.min_height <= height <= self.max_height:
            raise ValueError(f"La taille doit etre comprise entre {self.min_height} et {self.max_height} m.")
        return height

    def validate_age(self, age_value):
        try:
            age = int(str(age_value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError("L'age doit etre un nombre entier valide.") from exc
        if not self.min_age <= age <= self.max_age:
            raise ValueError(f"L'age doit etre compris entre {self.min_age} et {self.max_age} ans.")
        return age

    def validate_gender(self, gender_value):
        gender = str(gender_value).strip()
        if gender not in self.allowed_genders:
            raise ValueError("Le genre selectionne est invalide.")
        return gender

    def validate_activity(self, activity_value):
        activity = str(activity_value).strip()
        if activity not in self.allowed_activity_levels:
            raise ValueError("Le niveau d'activite selectionne est invalide.")
        return activity

    def validate_user_input(self, user_input):
        cleaned_data = {}
        errors = []

        field_validators = {
            "weight": self.validate_weight,
            "height": self.validate_height,
            "age": self.validate_age,
            "gender": self.validate_gender,
            "activity_level": self.validate_activity,
        }

        for field_name, validator in field_validators.items():
            field_value = user_input.get(field_name, "")
            if str(field_value).strip() == "":
                errors.append(f"Le champ '{field_name}' est obligatoire.")
                continue
            try:
                cleaned_data[field_name] = validator(field_value)
            except ValueError as error:
                errors.append(str(error))

        return cleaned_data, errors

    def _to_float(self, value, message):
        try:
            return float(str(value).strip().replace(",", "."))
        except (TypeError, ValueError) as exc:
            raise ValueError(message) from exc
