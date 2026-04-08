import csv
import sqlite3
from datetime import datetime
from pathlib import Path


class StorageService:
    def __init__(self, database_path, table_name="imc_records"):
        self.database_path = Path(database_path)
        self.table_name = table_name
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    activity_level TEXT NOT NULL,
                    bmi_value REAL NOT NULL,
                    bmi_category TEXT NOT NULL,
                    risk_level_rule TEXT NOT NULL,
                    risk_level_ml TEXT,
                    prediction_confidence REAL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def save_user_record(self, record_data):
        created_at = record_data.get("created_at") or datetime.now().isoformat(timespec="seconds")
        complete_record = {
            "weight": record_data["weight"],
            "height": record_data["height"],
            "age": record_data["age"],
            "gender": record_data["gender"],
            "activity_level": record_data["activity_level"],
            "bmi_value": record_data["bmi_value"],
            "bmi_category": record_data["bmi_category"],
            "risk_level_rule": record_data["risk_level_rule"],
            "risk_level_ml": record_data.get("risk_level_ml"),
            "prediction_confidence": record_data.get("prediction_confidence"),
            "created_at": created_at,
        }

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""
                INSERT INTO {self.table_name} (
                    weight,
                    height,
                    age,
                    gender,
                    activity_level,
                    bmi_value,
                    bmi_category,
                    risk_level_rule,
                    risk_level_ml,
                    prediction_confidence,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    complete_record["weight"],
                    complete_record["height"],
                    complete_record["age"],
                    complete_record["gender"],
                    complete_record["activity_level"],
                    complete_record["bmi_value"],
                    complete_record["bmi_category"],
                    complete_record["risk_level_rule"],
                    complete_record["risk_level_ml"],
                    complete_record["prediction_confidence"],
                    complete_record["created_at"],
                ),
            )
            connection.commit()
            record_id = cursor.lastrowid

        complete_record["id"] = record_id
        return complete_record

    def fetch_all_records(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def fetch_last_record(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY created_at DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetch_statistics(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                f"""
                SELECT
                    COUNT(*) AS total_records,
                    AVG(weight) AS avg_weight,
                    AVG(height) AS avg_height,
                    AVG(age) AS avg_age,
                    AVG(bmi_value) AS avg_bmi
                FROM {self.table_name}
                """
            )
            global_stats = dict(cursor.fetchone())

            cursor.execute(
                f"""
                SELECT bmi_category, COUNT(*) AS total
                FROM {self.table_name}
                GROUP BY bmi_category
                ORDER BY total DESC, bmi_category ASC
                """
            )
            by_category = [dict(row) for row in cursor.fetchall()]

            cursor.execute(
                f"""
                SELECT risk_level_rule, COUNT(*) AS total
                FROM {self.table_name}
                GROUP BY risk_level_rule
                ORDER BY total DESC, risk_level_rule ASC
                """
            )
            by_rule_risk = [dict(row) for row in cursor.fetchall()]

        return {
            "database_path": str(self.database_path),
            "table_name": self.table_name,
            "global": global_stats,
            "by_bmi_category": by_category,
            "by_risk_level_rule": by_rule_risk,
        }

    def get_user_history(self):
        return self.fetch_all_records()

    def count_total_records(self):
        return len(self.fetch_all_records())

    def calculate_average_bmi(self):
        stats = self.fetch_statistics()
        return stats["global"].get("avg_bmi")

    def count_by_bmi_category(self):
        stats = self.fetch_statistics()
        return stats["by_bmi_category"]

    def count_by_ml_prediction(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                f"""
                SELECT risk_level_ml, COUNT(*) AS total
                FROM {self.table_name}
                GROUP BY risk_level_ml
                ORDER BY total DESC, risk_level_ml ASC
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    def export_records_to_csv(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        records = self.fetch_all_records()

        fieldnames = [
            "id",
            "weight",
            "height",
            "age",
            "gender",
            "activity_level",
            "bmi_value",
            "bmi_category",
            "risk_level_rule",
            "risk_level_ml",
            "prediction_confidence",
            "created_at",
        ]

        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        return str(output_path)

    def save_application_record(self, record_data):
        user_input = record_data["user_input"]
        bmi_result = record_data["bmi_result"]
        prediction_result = record_data.get("prediction_result") or {}

        flattened_record = {
            "weight": user_input["weight"],
            "height": user_input["height"],
            "age": user_input["age"],
            "gender": user_input["gender"],
            "activity_level": user_input["activity_level"],
            "bmi_value": bmi_result["bmi_value"],
            "bmi_category": bmi_result["bmi_category"],
            "risk_level_rule": bmi_result["risk_level_rule"],
            "risk_level_ml": prediction_result.get("predicted_risk"),
            "prediction_confidence": prediction_result.get("confidence_score"),
            "created_at": record_data.get("created_at"),
        }
        return self.save_user_record(flattened_record)

    def save_result(self, user_profile, bmi_result, prediction_data=None):
        prediction_data = prediction_data or {}
        record_data = {
            "user_input": user_profile,
            "bmi_result": {
                **bmi_result,
                "risk_level_rule": bmi_result.get("risk_level_rule", bmi_result.get("risk_level")),
            },
            "prediction_result": {
                "predicted_risk": prediction_data.get("predicted_risk", prediction_data.get("risk_level_ml")),
                "confidence_score": prediction_data.get("confidence_score", prediction_data.get("prediction_confidence")),
            },
        }
        return self.save_application_record(record_data)
