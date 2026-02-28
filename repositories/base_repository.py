from database import get_connection

class BaseRepository:
    
    def execute_query(self, query, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params) if params else cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def execute_one(self, query, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params) if params else cursor.execute(query)
            return cursor.fetchone()
        finally:
            conn.close()
    
    def execute_write(self, query, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params) if params else cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
