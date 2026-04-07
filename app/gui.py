import tkinter as tk
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
        self.result_label = None
        self.prediction_label = None
        self.status_message = None

        self.current_user_profile = None
        self.current_result = None
        self.current_prediction = None

    def build_main_window(self):
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        self.root.title("Calculateur d'indice de masse corporelle")

        self.create_input_fields()
        self.create_result_section()
        self.create_buttons()

        self.status_message = tk.Label(self.root, text="Pret", fg="blue")
        self.status_message.pack(padx=15, pady=10, anchor="w")

        self.root.mainloop()

    def create_input_fields(self):
        params = tk.LabelFrame(self.root, text="Parametres", padx=10, pady=10)
        params.pack(padx=15, pady=10, fill="x", anchor="w")

        tk.Label(params, text="Poids (kg):").grid(row=0, column=0, sticky="w", pady=5)
        self.weight_input = tk.Entry(params)
        self.weight_input.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(params, text="Taille (m):").grid(row=1, column=0, sticky="w", pady=5)
        self.height_input = tk.Entry(params)
        self.height_input.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(params, text="Age:").grid(row=2, column=0, sticky="w", pady=5)
        self.age_input = tk.Entry(params)
        self.age_input.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(params, text="Genre:").grid(row=3, column=0, sticky="w", pady=5)
        self.gender_input = tk.StringVar(value="")
        gender_menu = tk.OptionMenu(params, self.gender_input, "Homme", "Femme", "Autre")
        gender_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(params, text="Activite:").grid(row=4, column=0, sticky="w", pady=5)
        self.activity_input = tk.StringVar(value="")
        activity_menu = tk.OptionMenu(params, self.activity_input, "Faible", "Moderee", "Elevee")
        activity_menu.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    def create_result_section(self):
        params2 = tk.LabelFrame(self.root, text="Resultats", padx=10, pady=10)
        params2.pack(padx=15, pady=10, fill="x", anchor="w")

        self.result_label = tk.Label(params2, text="Aucun resultat.", justify="left", anchor="w")
        self.result_label.grid(row=0, column=0, sticky="w", pady=5)

        self.prediction_label = tk.Label(params2, text="Aucune prediction.", justify="left", anchor="w")
        self.prediction_label.grid(row=1, column=0, sticky="w", pady=5)

    def create_buttons(self):
        params3 = tk.LabelFrame(self.root, text="", padx=10, pady=10)
        params3.grid_columnconfigure(0, weight=1)
        params3.pack(padx=15, pady=10, fill="x")

        tk.Button(params3, text="Quitter", command=self.root.quit).grid(row=0, column=1, pady=5)
        tk.Button(params3, text="Effacer", command=self.clear_form).grid(row=0, column=2, pady=5)
        tk.Button(params3, text="Calculer", command=self.on_calculate_clicked).grid(row=0, column=3, pady=5)
        tk.Button(params3, text="Predire", command=self.on_predict_clicked).grid(row=0, column=4, pady=5)
        tk.Button(params3, text="Sauvegarder", command=self.on_save_clicked).grid(row=0, column=5, pady=5)

    def on_calculate_clicked(self):
        user_input = {
            "weight": self.weight_input.get(),
            "height": self.height_input.get(),
            "age": self.age_input.get(),
            "gender": self.gender_input.get(),
            "activity_level": self.activity_input.get(),
        }

        cleaned_data, errors = self.services["validator"].validate_user_input(user_input)
        if errors:
            self.display_error("\n".join(errors))
            return

        bmi_result = self.services["imc_service"].build_bmi_result(
            cleaned_data["weight"],
            cleaned_data["height"],
        )
        recommendation_text = self.services["recommendation_service"].build_recommendation_text(
            cleaned_data,
            bmi_result,
        )

        result_data = {
            "user_profile": cleaned_data,
            "bmi_result": bmi_result,
            "recommendation_text": recommendation_text,
        }

        self.current_user_profile = cleaned_data
        self.current_result = result_data
        self.display_result(result_data)

    def on_predict_clicked(self):
        if not self.current_result:
            self.display_error("Calculez d'abord un resultat.")
            return

        prediction_data = {
            "message": "Prediction non disponible dans cette etape. Le module est reserve a la suite du projet."
        }
        self.current_prediction = prediction_data
        self.display_prediction(prediction_data)

    def on_save_clicked(self):
        if not self.current_result:
            self.display_error("Aucun resultat a sauvegarder.")
            return

        self.services["storage_service"].save_result(
            self.current_user_profile,
            self.current_result["bmi_result"],
        )
        self.status_message.config(text="Resultat sauvegarde.")

    def clear_form(self):
        self.weight_input.delete(0, "end")
        self.height_input.delete(0, "end")
        self.age_input.delete(0, "end")
        self.gender_input.set("")
        self.activity_input.set("")
        self.result_label.config(text="Aucun resultat.")
        self.prediction_label.config(text="Aucune prediction.")
        self.status_message.config(text="Formulaire efface.")
        self.current_user_profile = None
        self.current_result = None
        self.current_prediction = None

    def display_result(self, result_data):
        bmi_result = result_data["bmi_result"]
        recommendation_text = result_data["recommendation_text"]
        message = (
            f"Poids: {bmi_result['weight']} kg\n"
            f"Taille: {bmi_result['height']} m\n"
            f"IMC: {bmi_result['bmi_value']}\n"
            f"Categorie: {bmi_result['bmi_category']}\n"
            f"Risque: {bmi_result['risk_level']}\n\n"
            f"Recommandations:\n{recommendation_text}"
        )
        self.result_label.config(text=message)
        self.status_message.config(text="Calcul termine.")

    def display_prediction(self, prediction_data):
        self.prediction_label.config(text=prediction_data.get("message", "Aucune prediction."))
        self.status_message.config(text="Etat de prediction mis a jour.")

    def display_error(self, message):
        self.status_message.config(text=message)
        messagebox.showwarning("Warning", message)
