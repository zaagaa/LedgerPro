# middleware/db_router.py
# Router is now passive since protection moved to middleware

from middleware.readonly_protect import get_current_request

class ReadOnlyRouter:
    def db_for_write(self, model, **hints):
        return None  # All blocking handled in middleware

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
