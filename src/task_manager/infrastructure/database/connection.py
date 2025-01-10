# import psycopg2
# from psycopg2.extras import RealDictCursor


# class DatabaseConnection:
#     _instance = None

#     def __new__(cls, dsn):
#         if cls._instance is None:
#             cls._instance = super(DatabaseConnection, cls).__new__(cls)
#             cls._instance.dsn = dsn
#             cls._instance.connection = None
#         return cls._instance
    
#     def get_connection(self):
#         if self.connection is None or self.connection.closed:
#             self.connection = psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
#         return self.connectioin