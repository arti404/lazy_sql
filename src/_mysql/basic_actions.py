import trace
import mysql.connector
import logging, traceback


log = logging.getLogger(__name__)


class PropertyContainer:
    def __init__(self, data):
        # Store the kwargs data
        self._data = data

    def __getattr__(self, name):
        """Allow access to kwargs keys as attributes."""
        if name in self._data:
            # Return the value of the key, or the full dictionary if "value" doesn't exist
            return self._data[name].get("value", self._data[name])
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class BasicWrapper:
    """
    A basic wrapper for database operations.

    Args:
        host (str): The database host address.
        user (str): The username for database authentication.
        password (str): The password for the specified user.
        database (str): The name of the database to connect to.
        scheme (dict, optional): A dictionary representing the database table schema. Defaults to None.

    Example:
        ```python
        scheme = {
            "table1_name": {
                "column1_name": {
                    "type": "COLUMN_TYPE",
                    "default": False  # Optional; will be set as PRIMARY_KEY if True, must be unique
                },
            }
        }
        ```
    """
    def __init__(self, host:str, user:str, password:str, database:str, scheme:dict=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.TABLES = PropertyContainer(scheme) if scheme else None
    
    def connect(self):
        """connect to the database"""
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                database = self.database
            )
            self.connection.commit()
            self.cursor = self.connection.cursor()
            log.info(f"successfully connected to '{self.database}' at {self.host} as '{self.user}'")
            return (self.connection, self.cursor)
        except mysql.connector.Error as err:
            log.error(f"failed to connect to '{self.database}' at {self.host}: \n{err}", exc_info=True)
            self.connection = None
            self.cursor = None
            return
        except Exception as err:
            log.error(f"unexpected error while connecting to '{self.database}' at {self.host}: \n{err}")
            print(f"unexpected error while connecting to '{self.database}' at {self.host}: \n")
            traceback.print_exc()
            self.connection = None
            self.cursor = None
            return

    def disconnect(self):
        """disconnect from the database"""
        if self.connection:
            self.connection.close()


class Action(BasicWrapper):
    """base class for MySQL actions

    Args:
        host (str): The database host address.
        user (str): The username for database authentication.
        password (str): The password for the specified user.
        database (str): The name of the database to connect to.
        scheme (dict, optional): A dictionary representing the database table schema. Defaults to None.

    Example:
        ```python
        scheme = {
            "table1_name": {
                "column1_name": {
                    "type": "COLUMN_TYPE",
                    "default": False  # Optional; will be set as PRIMARY_KEY if True, must be unique
                },
            }
        }
        ```"""
    def __init__(self, host:str, user:str, password:str, database:str, scheme:dict=None):
        super().__init__(host, user, password, database, scheme)
    