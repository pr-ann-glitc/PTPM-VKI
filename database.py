import sqlite3 as sql

class DatabaseTriangle:
    def __init__(self, path):
        self._connection = sql.connect(path)
        self._connection.row_factory = sql.Row
        self._create_table()

    def _create_table(self):
        self._connection.execute('''
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                type TEXT, 
                exception TEXT,
                PRIMARY KEY (side1, side2, side3)  
            )
        ''')
        self._connection.commit()

    def add(self, side1: float, side2: float, side3: float, tri_type: str, exception: str = ""):
        self._connection.execute('''
        INSERT OR REPLACE INTO triangles 
        (side1, side2, side3, type, exception)
        VALUES (?, ?, ?, ?, ?)''',
(side1, side2, side3, tri_type, exception)
        )
        self._connection.commit()

    def get(self, side1: float, side2: float, side3: float):
        cursor = self._connection.execute('SELECT * FROM triangles'
                                          ' WHERE side1 = ? AND side2 = ? AND side3 = ?',
                                          (side1, side2, side3)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def delete (self, side1: float, side2: float, side3: float) -> bool:
        cursor = self._connection.execute('DELETE FROM triangles'
                                          ' WHERE side1 = ? AND side2 = ? AND side3 = ?',
                                          (side1, side2, side3)
                                          )
        self._connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self._connection.close()