from datetime import datetime

from SauvegardeIMC import SauvegardeIMC


class StorageService:
    def save_result(self, user_profile, bmi_result):
        current_time_string = str(datetime.now())
        data_imc = [
            current_time_string,
            str(user_profile["height"]),
            str(user_profile["weight"]),
            f"{bmi_result['bmi_value']:.2f}",
            bmi_result["bmi_category"],
            bmi_result["risk_level"],
        ]

        saver = SauvegardeIMC(data_imc)
        saver.sauvegarde_ficher()
        saver.sauvegarder_dataIMC(
            current_time_string,
            str(user_profile["height"]),
            str(user_profile["weight"]),
            f"{bmi_result['bmi_value']:.2f}",
            bmi_result["bmi_category"],
            bmi_result["risk_level"],
        )
        return {"saved_at": current_time_string}
