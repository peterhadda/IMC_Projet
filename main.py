from pathlib import Path

from app.gui import IMCApplicationGUI
from app.history_service import HistoryService
from app.imc_service import IMCService
from app.predictor_service import PredictorService
from app.recommendation_service import RecommendationService
from app.storage_service import StorageService
from app.validator import UserInputValidator


def load_configuration():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    raw_data_dir = data_dir / "raw"
    models_dir = base_dir / "models"
    default_db_path = data_dir / "data_imc.db"
    legacy_db_path = raw_data_dir / "data_imc.db"

    app_config = {
        "db_path": legacy_db_path if legacy_db_path.exists() else default_db_path,
        "export_csv_path": raw_data_dir / "records_export.csv",
        "model_path": models_dir / "best_model.pkl",
        "feature_config_path": models_dir / "feature_config.json",
        "evaluation_report_path": models_dir / "evaluation_report.json",
        "recommendation_path": raw_data_dir / "recommandations.json",
    }
    return app_config


def initialize_services():
    app_config = load_configuration()
    db_path = app_config["db_path"]
    model_path = app_config["model_path"]

    services = {
        "app_config": app_config,
        "db_path": db_path,
        "model_path": model_path,
        "validator": UserInputValidator(),
        "imc_service": IMCService(),
        "recommendation_service": RecommendationService(app_config["recommendation_path"]),
        "storage_service": StorageService(db_path),
    }
    services["history_service"] = HistoryService(services["storage_service"])
    services["predictor_service"] = PredictorService(
        model_path=app_config["model_path"],
        feature_config_path=app_config["feature_config_path"],
        evaluation_report_path=app_config["evaluation_report_path"],
    )
    return services


def start_application():
    services = initialize_services()
    application = IMCApplicationGUI(services)
    application.build_main_window()


if __name__ == "__main__":
    start_application()
