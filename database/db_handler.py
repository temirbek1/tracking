import sqlite3

class DatabaseHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            track_id INTEGER,
            image_path TEXT
        )
        """)
        self.conn.commit()

    def add_person(self, track_id, image_path):
        self.cursor.execute("INSERT INTO people (track_id, image_path) VALUES (?, ?)", (track_id, image_path))
        self.conn.commit()

    def exists(self, track_id):
        self.cursor.execute("SELECT 1 FROM people WHERE track_id = ?", (track_id,))
        return self.cursor.fetchone() is not None
