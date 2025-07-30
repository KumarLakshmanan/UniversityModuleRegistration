from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.operations import DatabaseOperations as MySQLDatabaseOperations
from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySQLDatabaseSchemaEditor
from django.db.backends.mysql.features import DatabaseFeatures as MySQLDatabaseFeatures
from django.db.backends.mysql.introspection import DatabaseIntrospection as MySQLDatabaseIntrospection


class DatabaseFeatures(MySQLDatabaseFeatures):
    """Custom features for MariaDB 10.4.32 compatibility"""
    
    # Disable features that require newer versions
    supports_over_clause = False
    supports_window_functions = False
    supports_json_field = False
    supports_json_field_contains = False
    supports_returning_columns = False
    supports_returning_into = False
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False
    
    def __init__(self, connection):
        super().__init__(connection)
        # Force disable RETURNING clause support
        self.can_return_columns_from_insert = False
        self.can_return_rows_from_bulk_insert = False


class DatabaseOperations(MySQLDatabaseOperations):
    """Custom operations for MariaDB 10.4.32 compatibility"""
    
    def bulk_insert_sql(self, fields, placeholder_rows):
        """Override to ensure no RETURNING clause is used"""
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql
    
    def insert_statement(self, ignore_conflicts=False, on_conflict=None):
        """Override to ensure no RETURNING clause and handle on_conflict"""
        if ignore_conflicts or on_conflict:
            return "INSERT IGNORE INTO"
        return "INSERT INTO"


class DatabaseSchemaEditor(MySQLDatabaseSchemaEditor):
    """Custom schema editor for MariaDB 10.4.32 compatibility"""
    pass


class DatabaseIntrospection(MySQLDatabaseIntrospection):
    """Custom introspection for MariaDB 10.4.32 compatibility"""
    pass


class DatabaseWrapper(MySQLDatabaseWrapper):
    """Custom database wrapper for MariaDB 10.4.32 compatibility"""
    
    # Use our custom classes
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations
    SchemaEditorClass = DatabaseSchemaEditor
    introspection_class = DatabaseIntrospection
    
    def check_database_version_supported(self):
        """Override to skip MariaDB version check"""
        # Skip the version check entirely
        pass
    
    def ensure_connection(self):
        """Override to handle connection setup"""
        if self.connection is None:
            with self.wrap_database_errors:
                self.connect()
        
        # Skip version checks
        return
    
    def init_connection_state(self):
        """Override to skip version-dependent initialization"""
        assignments = []
        
        # Set SQL mode
        if self.settings_dict.get('OPTIONS', {}).get('sql_mode'):
            sql_mode = self.settings_dict['OPTIONS']['sql_mode']
            assignments.append('sql_mode = %s')
            
        # Set character set
        charset = self.settings_dict.get('OPTIONS', {}).get('charset', 'utf8mb4')
        assignments.append('character_set_connection = %s')
        
        if assignments:
            with self.cursor() as cursor:
                if self.settings_dict.get('OPTIONS', {}).get('sql_mode'):
                    cursor.execute('SET ' + ', '.join(assignments), 
                                   [sql_mode, charset])
                else:
                    cursor.execute('SET ' + assignments[0], [charset])
