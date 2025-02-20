import sqlite3


class BaseWrapper:
    """a basic wrapper for database operations"""
    def __init__(self, db_name, **kwargs):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.tables = kwargs["tables"] if "tables" in kwargs else None
        return self.cursor
    
    def command(self, prompt:str):
        """execute a command"""
        self.cursor.execute(prompt)
    
    def commit(self, prompt:str):
        """execute a command and commit the changes"""
        self.cursor.execute(prompt)
        self.connection.commit()
    
    def disconnect(self):
        self.connection.close()


class Action(BaseWrapper):
    """a main wrapper for sqlite3"""
    def __init__(self, db_name, **kwargs):
        super().__init__(db_name, kwargs=kwargs)
    
    def create_table(self, table_name:str, columns:list[dict|tuple]):
        """
        Create a table with the given columns.

        Args:
            table_name (str): The name of the table to be created.
            columns (list): A list of dictionaries or tuples, each containing the column name and type.

        Column Definition Examples:
            ```python
            # Dictionary format:
            {
                'name': 'column_name',
                'type': 'column_type',  # e.g., BIGINT, INTEGER, REAL, TEXT, BLOB, etc.
                'primary': True  # Optional; if True, this column will be PRIMARY KEY (must be UNIQUE)
            }
            
            # Tuple format:
            ('column_name', 'column_type')
            ```
        """
        tables = str()
        for column in columns:
            if isinstance(column, dict):
                if "primary" in column and (column["primary"]==True or column["primary"]=="True"):
                    tables += f"{column['name']} {column['type']} PRIMARY KEY,"
                else:
                    tables += f"{column['name']} {column['type']},"
            if isinstance(column, tuple):
                tables += f"{column[0]} {column[1]},"
        self.commit(f"CREATE TABLE IF NOT EXISTS {table_name} ({tables[:-1]})")
    #TODO: finish this wrapper
