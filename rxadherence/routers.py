class Router(object):
    """
    Determine how to route database calls for an app's models (in this case, for an app named rxadherence).
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    https://strongarm.io/blog/multiple-databases-in-django/
    https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#multiple-databases
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on rxadherence app models to `rxadherence_db`."""
        if model._meta.app_label == 'rxadherence':
            return 'rxadherence_db'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on rxadherence app models to `rxadherence_db`."""
        if model._meta.app_label == 'rxadherence':
            return 'rxadherence_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""

        if obj1._meta.model_name.lower().startswith('pmkb') and obj2._meta.model_name.lower().startswith('pmkb'):
            return True

        # Allow any relation between two models that are both in the rxadherence app.
        if obj1._meta.app_label == 'rxadherence' and obj2._meta.app_label == 'rxadherence':
            return True
        # No opinion if neither object is in the rxadherence app (defer to default or other routers).
        elif 'rxadherence' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the rxadherence app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the rxadherence app's models get created on the right database."""
        # print("db:{db}, app_label:{app_label}, model_name:{model_name}".format(db=db, app_label=app_label, model_name=model_name))
        # The rxadherence app should be migrated only on the rxadherence_db database.
        if app_label == 'rxadherence':
            return db == 'rxadherence_db'

        # No opinion for all other scenarios
        return None
