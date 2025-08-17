import sqlite3

class DBManager:
    def __init__(self, db_name="score.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Cria tabela se não existir"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER
            )
        """)
        self.conn.commit()

    def save_score(self, score):
        """Salva score no banco"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
        self.conn.commit()

    def get_high_score(self):
        """Retorna o maior score já salvo"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(score) FROM scores")
        result = cursor.fetchone()[0]
        return result if result else 0

    def close(self):
        """Fecha conexão com o banco"""
        self.conn.close()
