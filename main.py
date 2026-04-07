from pathlib import Path

from app.gui import IMCApplicationGUI
from app.imc_service import IMCService
from app.recommendation_service import RecommendationService
from app.storage_service import StorageService
from app.validator import UserInputValidator


def load_configuration():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    app_config = {
        "db_path": data_dir / "data_imc.db",
        "model_path": None,
        "recommendation_path": data_dir / "recommandations.json",
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
    return services


def start_application():
    services = initialize_services()
    application = IMCApplicationGUI(services)
    application.build_main_window()


if __name__ == "__main__":
    start_application()
