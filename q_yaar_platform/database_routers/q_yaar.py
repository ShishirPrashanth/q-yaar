class QYaarRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    route_app_labels = {"account", "jwt_auth", "profile_player"}

    def db_for_read(self, model, **hints):
        """
        All reads to `default`
        """
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None

    def db_for_write(self, model, **hints):
        """
        No writes for geo
        """
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        No relations from outside geo
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        No migrations, geo is externally managed
        """
        return db == "default" and app_label in self.route_app_labels
