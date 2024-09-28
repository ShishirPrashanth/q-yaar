class GeodbRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def db_for_read(self, model, **hints):
        """
        All reads from `geo`
        """
        if model._meta.app_label == "geodb":
            return "geo"
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
            obj1._meta.app_label == "geo"
            and obj2._meta.app_label == "geo"
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        No migrations, geo is externally managed
        """
        return None
