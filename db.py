import sqlite3

def create_database():
    conn = sqlite3.connect("articles.db")  # crée le fichier articles.db s’il n’existe pas
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            publication_date TEXT,
            summary TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_article(article):
    try:
        conn = sqlite3.connect("articles.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO articles (title, url, publication_date, summary, source)
            VALUES (?, ?, ?, ?, ?)
        """, (article["title"], article["url"], article["publication_date"], article["summary"], article["source"]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l’insertion dans la BDD : {e}")

def fetch_all_articles():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
