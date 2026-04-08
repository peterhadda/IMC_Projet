import tkinter as tk
from datetime import datetime
from tkinter import messagebox


class IMCApplicationGUI:
    def __init__(self, services):
        self.services = services
        self.root = tk.Tk()

        self.weight_input = None
        self.height_input = None
        self.age_input = None
        self.gender_input = None
        self.activity_input = None

        self.result_label = tk.StringVar(value="IMC: -")
        self.prediction_label = tk.StringVar(value="Prediction ML: -")
        self.status_message = tk.StringVar(value="Pret.")
        self.category_label = tk.StringVar(value="Categorie: -")
        self.rule_risk_label = tk.StringVar(value="Risque classique: -")
        self.recommendation_label = tk.StringVar(value="Recommandation: -")
        self.confidence_label = tk.StringVar(value="Confiance modele: -")

        self.current_user_input = None
        self.current_bmi_result = None
        self.current_prediction_result = None
        self.current_recommendation_text = ""

    def build_main_window(self):
        self.root.geometry("1080x760")
        self.root.resizable(False, False)
        self.root.title("Calculateur IMC et Prediction ML")

        self.create_input_fields()
        self.create_result_section()
        self.create_buttons()

        status_bar = tk.Label(self.root, textvariable=self.status_message, fg="blue", anchor="w")
        status_bar.pack(fill="x", padx=15, pady=(6, 12))

        self.root.mainloop()

    def create_input_fields(self):
        params = tk.LabelFrame(self.root, text="Donnees utilisateur", padx=12, pady=12)
        params.pack(padx=15, pady=12, fill="x", anchor="w")

        tk.Label(params, text="Poids (kg):").grid(row=0, column=0, sticky="w", pady=6)
        self.weight_input = tk.Entry(params, width=20)
        self.weight_input.grid(row=0, column=1, padx=10, pady=6, sticky="w")

        tk.Label(params, text="Taille (m):").grid(row=1, column=0, sticky="w", pady=6)
        self.height_input = tk.Entry(params, width=20)
        self.height_input.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        tk.Label(params, text="Age:").grid(row=2, column=0, sticky="w", pady=6)
        self.age_input = tk.Entry(params, width=20)
        self.age_input.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        tk.Label(params, text="Sexe:").grid(row=3, column=0, sticky="w", pady=6)
        self.gender_input = tk.StringVar(value="")
        tk.OptionMenu(params, self.gender_input, "Homme", "Femme", "Autre").grid(
            row=3,
            column=1,
            padx=10,
            pady=6,
            sticky="w",
        )

        tk.Label(params, text="Niveau d'activite:").grid(row=4, column=0, sticky="w", pady=6)
        self.activity_input = tk.StringVar(value="")
        tk.OptionMenu(params, self.activity_input, "Faible", "Moderee", "Elevee").grid(
            row=4,
            column=1,
            padx=10,
            pady=6,
            sticky="w",
        )

    def create_result_section(self):
        results_frame = tk.LabelFrame(self.root, text="Analyse", padx=12, pady=12)
        results_frame.pack(padx=15, pady=12, fill="both", expand=True)

        tk.Label(results_frame, textvariable=self.result_label, justify="left", anchor="w").pack(anchor="w", pady=4)
        tk.Label(results_frame, textvariable=self.category_label, justify="left", anchor="w").pack(anchor="w", pady=4)
        tk.Label(results_frame, textvariable=self.rule_risk_label, justify="left", anchor="w").pack(anchor="w", pady=4)
        tk.Label(
            results_frame,
            textvariable=self.recommendation_label,
            justify="left",
            anchor="w",
            wraplength=980,
        ).pack(anchor="w", pady=4)
        tk.Label(results_frame, textvariable=self.prediction_label, justify="left", anchor="w").pack(anchor="w", pady=10)
        tk.Label(results_frame, textvariable=self.confidence_label, justify="left", anchor="w").pack(anchor="w", pady=4)

    def create_buttons(self):
        buttons_frame = tk.LabelFrame(self.root, text="Actions", padx=12, pady=12)
        buttons_frame.pack(padx=15, pady=12, fill="x")

        tk.Button(buttons_frame, text="Calculer IMC", command=self.on_calculate_clicked).grid(row=0, column=0, padx=6, pady=6)
        tk.Button(buttons_frame, text="Predire avec ML", command=self.on_predict_clicked).grid(row=0, column=1, padx=6, pady=6)
        tk.Button(buttons_frame, text="Sauvegarder", command=self.on_save_clicked).grid(row=0, column=2, padx=6, pady=6)
        tk.Button(buttons_frame, text="Voir historique", command=self.on_view_history_clicked).grid(row=0, column=3, padx=6, pady=6)
        tk.Button(buttons_frame, text="Exporter CSV", command=self.on_export_csv_clicked).grid(row=0, column=4, padx=6, pady=6)
        tk.Button(buttons_frame, text="Reinitialiser", command=self.clear_form).grid(row=0, column=5, padx=6, pady=6)
        tk.Button(buttons_frame, text="Quitter", command=self.root.destroy).grid(row=0, column=6, padx=6, pady=6)

    def _read_user_fields(self):
        return {
            "weight": self.weight_input.get(),
            "height": self.height_input.get(),
            "age": self.age_input.get(),
            "gender": self.gender_input.get(),
            "activity_level": self.activity_input.get(),
        }

    def _build_validated_user_input(self):
        raw_user_input = self._read_user_fields()
        cleaned_data, errors = self.services["validator"].validate_user_input(raw_user_input)
        if errors:
            self.display_error("\n".join(errors))
            return None
        return cleaned_data

    def _build_classical_result(self, user_input):
        bmi_result = self.services["imc_service"].build_bmi_result(
            user_input["weight"],
            user_input["height"],
        )
        recommendation_text = self.services["recommendation_service"].build_recommendation_text(
            user_input,
            bmi_result,
        )
        return bmi_result, recommendation_text

    def _map_rule_to_ml_label(self, risk_level_rule):
        mapping = {
            "Moindre": "low_risk",
            "Accru": "moderate_risk",
            "Eleve": "high_risk",
            "Tres eleve": "high_risk",
            "Extremement eleve": "high_risk",
        }
        return mapping.get(risk_level_rule)

    def on_calculate_clicked(self):
        user_input = self._build_validated_user_input()
        if user_input is None:
            return

        bmi_result, recommendation_text = self._build_classical_result(user_input)

        self.current_user_input = user_input
        self.current_bmi_result = bmi_result
        self.current_prediction_result = None
        self.current_recommendation_text = recommendation_text

        self.display_result(
            {
                "user_input": user_input,
                "bmi_result": bmi_result,
                "recommendation_text": recommendation_text,
            }
        )
        self.display_prediction(None)
        self.status_message.set("Calcul IMC termine.")

    def on_predict_clicked(self):
        user_input = self.current_user_input or self._build_validated_user_input()
        if user_input is None:
            return

        if self.current_bmi_result is None or self.current_user_input != user_input:
            bmi_result, recommendation_text = self._build_classical_result(user_input)
            self.current_user_input = user_input
            self.current_bmi_result = bmi_result
            self.current_recommendation_text = recommendation_text
            self.display_result(
                {
                    "user_input": user_input,
                    "bmi_result": bmi_result,
                    "recommendation_text": recommendation_text,
                }
            )

        try:
            prediction_result = self.services["predictor_service"].predict_risk(user_input)
        except Exception as error:
            self.current_prediction_result = None
            self.display_error(str(error))
            return

        classical_label = self._map_rule_to_ml_label(self.current_bmi_result["risk_level_rule"])
        comparison_message = None
        if classical_label is not None:
            if classical_label == prediction_result["predicted_risk"]:
                comparison_message = "Comparaison: la regle classique et le modele ML sont alignes."
            else:
                comparison_message = "Comparaison: la regle classique et le modele ML divergent."

        prediction_result["comparison_message"] = comparison_message
        self.current_prediction_result = prediction_result
        self.display_prediction(prediction_result)
        self.status_message.set("Prediction ML terminee.")

    def on_save_clicked(self):
        if self.current_user_input is None or self.current_bmi_result is None:
            self.display_error("Calculez d'abord un resultat avant de sauvegarder.")
            return

        record_data = {
            "user_input": self.current_user_input,
            "bmi_result": self.current_bmi_result,
            "recommendation_text": self.current_recommendation_text,
            "prediction_result": self.current_prediction_result,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        saved_record = self.services["storage_service"].save_application_record(record_data)
        self.status_message.set(f"Resultat sauvegarde sous l'identifiant {saved_record['id']}.")

    def on_view_history_clicked(self):
        history_rows = self.services["history_service"].get_user_history()
        total_records = self.services["history_service"].count_total_records()
        average_bmi = self.services["history_service"].calculate_average_bmi()
        category_distribution = self.services["history_service"].count_by_bmi_category()
        prediction_distribution = self.services["history_service"].count_by_ml_prediction()

        history_window = tk.Toplevel(self.root)
        history_window.title("Historique et statistiques")
        history_window.geometry("900x620")

        history_text = tk.Text(history_window, wrap="word")
        history_text.pack(fill="both", expand=True, padx=12, pady=12)

        history_text.insert("end", f"Total enregistrements: {total_records}\n")
        if average_bmi is not None:
            history_text.insert("end", f"IMC moyen: {average_bmi:.2f}\n\n")
        else:
            history_text.insert("end", "IMC moyen: N/A\n\n")

        history_text.insert("end", "Distribution par categorie IMC:\n")
        for item in category_distribution:
            history_text.insert("end", f"- {item['bmi_category']}: {item['total']}\n")

        history_text.insert("end", "\nDistribution par prediction ML:\n")
        for item in prediction_distribution:
            label = item["risk_level_ml"] if item["risk_level_ml"] else "Aucune prediction"
            history_text.insert("end", f"- {label}: {item['total']}\n")

        history_text.insert("end", "\nDerniers enregistrements:\n")
        for row in history_rows[:10]:
            history_text.insert(
                "end",
                (
                    f"[{row['created_at']}] age={row['age']}, poids={row['weight']}, taille={row['height']}, "
                    f"imc={row['bmi_value']}, cat={row['bmi_category']}, "
                    f"regle={row['risk_level_rule']}, ml={row['risk_level_ml']}\n"
                ),
            )

        history_text.config(state="disabled")
        self.status_message.set("Historique affiche.")

    def on_export_csv_clicked(self):
        export_path = self.services["app_config"]["export_csv_path"]
        exported_file = self.services["storage_service"].export_records_to_csv(export_path)
        self.status_message.set(f"Export CSV realise: {exported_file}")

    def clear_form(self):
        self.weight_input.delete(0, "end")
        self.height_input.delete(0, "end")
        self.age_input.delete(0, "end")
        self.gender_input.set("")
        self.activity_input.set("")

        self.result_label.set("IMC: -")
        self.category_label.set("Categorie: -")
        self.rule_risk_label.set("Risque classique: -")
        self.recommendation_label.set("Recommandation: -")
        self.prediction_label.set("Prediction ML: -")
        self.confidence_label.set("Confiance modele: -")
        self.status_message.set("Formulaire reinitialise.")

        self.current_user_input = None
        self.current_bmi_result = None
        self.current_prediction_result = None
        self.current_recommendation_text = ""

    def display_result(self, result_data):
        bmi_result = result_data["bmi_result"]
        recommendation_text = result_data["recommendation_text"]

        self.result_label.set(f"IMC: {bmi_result['bmi_value']}")
        self.category_label.set(f"Categorie: {bmi_result['bmi_category']}")
        self.rule_risk_label.set(f"Risque classique: {bmi_result['risk_level_rule']}")
        self.recommendation_label.set(f"Recommandation: {recommendation_text}")

    def display_prediction(self, prediction_data):
        if not prediction_data:
            self.prediction_label.set("Prediction ML: -")
            self.confidence_label.set("Confiance modele: -")
            return

        formatted_output = self.services["predictor_service"].format_prediction_output(prediction_data)
        self.prediction_label.set(formatted_output)

        confidence_score = prediction_data.get("confidence_score")
        confidence_text = "N/A" if confidence_score is None else f"{confidence_score:.2%}"
        comparison_message = prediction_data.get("comparison_message")
        if comparison_message:
            self.confidence_label.set(f"Confiance modele: {confidence_text} | {comparison_message}")
        else:
            self.confidence_label.set(f"Confiance modele: {confidence_text}")

    def display_error(self, message):
        self.status_message.set(message)
        messagebox.showwarning("Erreur", message)
