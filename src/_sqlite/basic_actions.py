import sqlite3


class BaseWrapper:
    """a basic wrapper for database operations"""
    def __init__(self, db_name, **kwargs):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.tables = kwargs["tables"] if "tables" in kwargs else None
        return self.cursor
    
    def command(self, prompt:str):
        """execute a command and return the result if it's meant to return anything"""
        return self.cursor.execute(prompt)
    
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
        return self.cursor
    
    def create_table(self, table_name:str, columns:list[dict|tuple]):
        """
        create a table with the given columns
        -----------------
        :param table_name: the name of the table
        :param columns: a list of dictionaries or tuples, each containing the column name and type\n
        -----------------
        column_dict_hint: {
            'name': 'column_name',
            'type': 'column_type(BIGINT, INTEGER, REAL, TEXT, BLOB, etc.)'
            'primary'(optional): True(if u need it, must be UNIQUE for table, so will be used only the first one if couple are specified)
        }
        column_tuple_hint: ('column_name', 'column_type')
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
