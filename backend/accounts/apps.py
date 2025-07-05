# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# Don't forget to add to settings.py:
# AUTH_USER_MODEL = 'accounts.User'