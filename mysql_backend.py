from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper


class DatabaseWrapper(MySQLDatabaseWrapper):
    def check_database_version_supported(self):
        """Override to skip MariaDB version check"""
        pass
