import sqlite3

class DatabaseHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            track_id INTEGER UNIQUE,
            photo BLOB
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def exists(self, track_id):
        query = "SELECT 1 FROM people WHERE track_id = ?"
        result = self.conn.execute(query, (track_id,)).fetchone()
        return result is not None

    def add_person(self, track_id, photo):
        query = "INSERT INTO people (track_id, photo) VALUES (?, ?)"
        self.conn.execute(query, (track_id, photo.tobytes()))
        self.conn.commit()
