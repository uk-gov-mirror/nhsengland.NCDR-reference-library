from django.apps import apps
from django.utils.functional import SimpleLazyObject


class ModelContextProcessor(object):
    def __init__(self):
        for app_label, models in apps.all_models.items():
            setattr(self, app_label, models)


def models(request):
    return {"models": SimpleLazyObject(ModelContextProcessor)}