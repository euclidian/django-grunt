from django.conf import settings as django_settings


class LazySettings(object):

    @property
    def grunt_modules(self):
        return getattr(django_settings, "GRUNT_MODULES", {})

    @property
    def grunt_base_url(self):
        return getattr(django_settings, "GRUNT_BASE_URL", "")

settings = LazySettings()