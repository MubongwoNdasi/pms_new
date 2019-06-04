from django.apps import AppConfig


class DrugConfig(AppConfig):
    name = 'drug'

    def ready(self):
        import drug.signals


