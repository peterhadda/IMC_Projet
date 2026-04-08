class HistoryService:
    def __init__(self, storage_service):
        self.storage_service = storage_service

    def get_user_history(self):
        return self.storage_service.get_user_history()

    def count_total_records(self):
        return self.storage_service.count_total_records()

    def calculate_average_bmi(self):
        return self.storage_service.calculate_average_bmi()

    def count_by_bmi_category(self):
        return self.storage_service.count_by_bmi_category()

    def count_by_ml_prediction(self):
        return self.storage_service.count_by_ml_prediction()
