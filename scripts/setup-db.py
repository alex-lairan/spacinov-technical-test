#!/usr/bin/env python3
import sqlite3

DB_PATH = "data/phone_alloc.db"

def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS number_range (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start INTEGER NOT NULL,
        end INTEGER NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS allocated_number (
        number INTEGER PRIMARY KEY,
        range_id INTEGER,
        customer_id INTEGER,
        allocated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (range_id) REFERENCES number_range(id)
    );
    """)

    conn.commit()

def seed_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM number_range")
    (count,) = cur.fetchone()

    if count == 0:
        cur.execute("INSERT INTO number_range (start, end) VALUES (?, ?)", (162050000, 162059999))
        cur.execute("INSERT INTO number_range (start, end) VALUES (?, ?)", (939010000, 939019999))
        conn.commit()
        print("Plages de numéros insérées dans la base.")
    else:
        print("Des plages existent déjà dans la table number_range.")

def setup_db(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    print(f"Connexion à la base SQLite '{db_path}' réussie.")
    create_tables(conn)
    seed_tables(conn)
    conn.close()
    print("Configuration de la base terminée.")

if __name__ == "__main__":
    setup_db()
